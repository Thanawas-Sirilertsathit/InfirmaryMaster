from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import authenticate
from patients.models import Patient
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'verified']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def _get_matching_patient(self, validated_data):
        role = (validated_data.get('role') or '').lower()
        first_name = (validated_data.get('first_name') or '').strip()
        last_name = (validated_data.get('last_name') or '').strip()

        if role != User.ROLE_PATIENT or not first_name or not last_name:
            return None

        matches = Patient.objects.select_related('user').filter(
            user__first_name__iexact=first_name,
            user__last_name__iexact=last_name,
        )

        if matches.count() > 1:
            raise serializers.ValidationError({
                'first_name': 'Multiple patient records match this first and last name.',
                'last_name': 'Multiple patient records match this first and last name.',
            })

        return matches.first()

    def validate(self, attrs):
        attrs['username'] = attrs['username'].strip()
        attrs['first_name'] = attrs['first_name'].strip()
        attrs['last_name'] = attrs['last_name'].strip()
        attrs['email'] = attrs['email'].strip()

        if attrs['role'].lower() == 'admin':
            raise serializers.ValidationError({'role': 'You cannot register as an admin.'})

        matched_patient = self._get_matching_patient(attrs)
        username_conflicts = User.objects.filter(username=attrs['username'])
        if matched_patient:
            username_conflicts = username_conflicts.exclude(pk=matched_patient.user_id)

        if username_conflicts.exists():
            raise serializers.ValidationError({'username': 'A user with that username already exists.'})

        self._matched_patient = matched_patient
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        matched_patient = getattr(self, '_matched_patient', None)
        if matched_patient:
            user = matched_patient.user
            user.username = validated_data['username']
            user.email = validated_data['email']
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.role = validated_data['role']
            user.verified = validated_data['role'] != User.ROLE_STAFF
            user.set_password(validated_data['password'])
            user.save()
            return user

        if validated_data['role'] == User.ROLE_STAFF:
            validated_data['verified'] = False

        user = User.objects.create_user(**validated_data)
        if user.role == User.ROLE_PATIENT:
            Patient.objects.get_or_create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include username and password.')
        return data