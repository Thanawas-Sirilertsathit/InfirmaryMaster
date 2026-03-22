from rest_framework import serializers
from .models import Prescription, PrescriptionItem
from medicines.models import Medicine
from patients.models import Patient


class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_dosage = serializers.CharField(source='medicine.dosage', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine', 'medicine_name', 'medicine_dosage', 'quantity', 'instruction']


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    prescribed_by_name = serializers.CharField(source='prescribed_by.get_full_name', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'patient_name', 'prescribed_by', 'prescribed_by_name', 'created_at', 'notes', 'items']
        read_only_fields = ['id', 'created_at', 'prescribed_by']


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['patient', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        prescription = Prescription.objects.create(
            prescribed_by=self.context['request'].user,
            **validated_data
        )
        for item_data in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)
        return prescription