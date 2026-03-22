from rest_framework import serializers
from .models import Medicine, MedicineCategory


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = ['id', 'name', 'description']


class MedicineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Medicine
        fields = ['id', 'category', 'category_name', 'name', 'dosage', 'description', 'minimum_stock', 'created_at']
        read_only_fields = ['id', 'created_at']