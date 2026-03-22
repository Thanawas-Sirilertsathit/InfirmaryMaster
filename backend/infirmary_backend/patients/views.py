from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Patient
from .serializers import PatientSerializer
from users.permissions import IsStaffOrAdmin, IsOwnPatientData


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrAdmin]


class PatientSearchView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        fname = self.request.query_params.get('fname', '')
        lname = self.request.query_params.get('lname', '')
        queryset = Patient.objects.all()
        if fname or lname:
            queryset = queryset.filter(
                Q(user__first_name__icontains=fname) & Q(user__last_name__icontains=lname)
            )
        return queryset


class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrAdmin]


class PatientPrescriptionsView(generics.ListAPIView):
    serializer_class = PatientSerializer  # We'll need prescription serializer later
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        if self.request.user.is_patient:
            # Patients can only see their own
            if not Patient.objects.filter(id=patient_id, user=self.request.user).exists():
                return Patient.objects.none()
        return Patient.objects.filter(id=patient_id)