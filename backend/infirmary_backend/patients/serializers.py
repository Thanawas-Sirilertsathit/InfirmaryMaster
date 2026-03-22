from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'medical_record_number', 'date_of_birth', 'emergency_contact', 'notes', 'user_full_name', 'username']
        read_only_fields = ['id']