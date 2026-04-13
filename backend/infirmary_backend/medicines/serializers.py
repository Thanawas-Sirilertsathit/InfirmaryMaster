from rest_framework import serializers
from .models import Medicine


class MedicineSerializer(serializers.ModelSerializer):
    image = serializers.URLField(required=False, allow_null=True)
    side_effects = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Medicine
        fields = ['id', 'category', 'name', 'dosage', 'description', 'minimum_stock', 'created_at', 'image', 'side_effects']
        read_only_fields = ['id', 'created_at']