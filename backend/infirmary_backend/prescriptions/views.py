from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Prescription
from .serializers import PrescriptionSerializer, PrescriptionCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsStaffOrAdmin, IsPatient
import logging

logger = logging.getLogger(__name__)


class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionCreateSerializer
    permission_classes = [IsStaffOrAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error('Validation error: %s', serializer.errors)  # Log validation errors
            raise e
        self.perform_create(serializer)
        data = PrescriptionSerializer(serializer.instance, context=self.get_serializer_context()).data
        headers = self.get_success_headers(data)
        return Response({"message": "Prescription created successfully", "data": data}, status=status.HTTP_201_CREATED, headers=headers)


class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        queryset = Prescription.objects.all()
        medicine = self.request.query_params.get('medicine')
        patient_name = self.request.query_params.get('patient_name')

        if medicine:
            queryset = queryset.filter(items__medicine__name__icontains=medicine).distinct()
        if patient_name:
            queryset = queryset.filter(
                Q(patient__user__first_name__icontains=patient_name) |
                Q(patient__user__last_name__icontains=patient_name)
            )
        return queryset


class PrescriptionDetailView(generics.RetrieveAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsStaffOrAdmin]


class PatientPrescriptionsView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        if self.request.user.is_patient:
            # Patients can only see their own prescriptions
            if not hasattr(self.request.user, 'patient_profile') or self.request.user.patient_profile.id != patient_id:
                return Prescription.objects.none()
        return Prescription.objects.filter(patient_id=patient_id)