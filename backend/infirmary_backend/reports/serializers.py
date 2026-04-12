from rest_framework import serializers

from .models import ReportNotification


class ReportNotificationSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_dosage = serializers.CharField(source='medicine.dosage', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    expiration_date = serializers.DateField(source='batch.expiration_date', read_only=True)

    class Meta:
        model = ReportNotification
        fields = [
            'id',
            'type',
            'title',
            'message',
            'is_read',
            'created_at',
            'medicine_name',
            'medicine_dosage',
            'batch_number',
            'expiration_date',
        ]