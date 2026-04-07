from rest_framework import serializers
from .models import MedicineBatch, StockTransaction, get_available_stock
from medicines.models import Medicine


class MedicineBatchSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_dosage = serializers.CharField(source='medicine.dosage', read_only=True)
    medicine_image = serializers.URLField(source='medicine.image', read_only=True, allow_null=True)

    class Meta:
        model = MedicineBatch
        fields = ['id', 'medicine', 'medicine_name', 'medicine_dosage', 'medicine_image', 'batch_number', 'quantity', 'expiration_date', 'added_at']
        read_only_fields = ['id', 'added_at']


class StockTransactionSerializer(serializers.ModelSerializer):
    batch_medicine = serializers.CharField(source='batch.medicine.name', read_only=True)

    class Meta:
        model = StockTransaction
        fields = ['id', 'batch', 'batch_medicine', 'transaction_type', 'quantity', 'reference', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class InventorySummarySerializer(serializers.Serializer):
    medicine_id = serializers.IntegerField()
    medicine_name = serializers.CharField()
    total_stock = serializers.IntegerField()
    expiring_soon = serializers.IntegerField()  # within 30 days
    expiring_later = serializers.IntegerField()  # 31-60 days