import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from inventory.models import MedicineBatch, deduct_stock
from patients.models import Patient

from .models import Prescription, PrescriptionItem

logger = logging.getLogger(__name__)

User = get_user_model()


class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine = serializers.IntegerField(source='medicine_id', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_dosage = serializers.CharField(source='medicine.dosage', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine', 'medicine_name', 'medicine_dosage', 'quantity', 'instruction']


class PrescriptionCreateItemSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    instruction = serializers.CharField(max_length=128, allow_blank=True, required=False)

    def validate_batch_id(self, value):
        if not MedicineBatch.objects.filter(id=value).exists():
            raise serializers.ValidationError('Invalid batch_id.')
        return value


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    prescribed_by_name = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    def get_prescribed_by_name(self, obj):
        full_name = obj.prescribed_by.get_full_name().strip()
        if full_name:
            return full_name
        return obj.prescribed_by.username

    def get_doctor(self, obj):
        return self.get_prescribed_by_name(obj)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'patient_name', 'prescribed_by', 'prescribed_by_name', 'doctor', 'created_at', 'notes', 'items']
        read_only_fields = ['id', 'created_at', 'prescribed_by']


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    items = PrescriptionCreateItemSerializer(many=True)
    patient_name = serializers.CharField(write_only=True)

    class Meta:
        model = Prescription
        fields = ['patient_name', 'notes', 'items']

    @transaction.atomic
    def create(self, validated_data):
        patient_name = validated_data.pop('patient_name')
        items_data = validated_data.pop('items')

        first_name, last_name = patient_name.split(' ', 1) if ' ' in patient_name else (patient_name, '')
        username = f'{first_name.lower()}_{last_name.lower()}' if last_name else first_name.lower()

        user, _ = User.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            defaults={'username': username},
        )
        patient, _ = Patient.objects.get_or_create(user=user)

        prescription = Prescription.objects.create(
            patient=patient,
            prescribed_by=self.context['request'].user,
            **validated_data,
        )

        for item_data in items_data:
            batch = MedicineBatch.objects.select_related('medicine').get(id=item_data['batch_id'])
            deduct_stock(batch.id, item_data['quantity'], reference=f'prescription:{prescription.id}')

            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine_id=batch.medicine_id,
                quantity=item_data['quantity'],
                instruction=item_data.get('instruction', ''),
            )

        return prescription
