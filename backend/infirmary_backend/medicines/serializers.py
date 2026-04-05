from rest_framework import serializers
from .models import Medicine, MedicineCategory


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = ['id', 'name', 'description']


class MedicineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.URLField(required=False, allow_null=True)
    side_effects = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Medicine
        fields = ['id', 'category', 'category_name', 'name', 'dosage', 'description', 'minimum_stock', 'created_at', 'image', 'side_effects']
        read_only_fields = ['id', 'created_at']