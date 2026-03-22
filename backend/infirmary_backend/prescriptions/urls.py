from django.urls import path
from .views import PrescriptionCreateView, PrescriptionListView, PrescriptionDetailView, PatientPrescriptionsView

urlpatterns = [
    path('', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('list/', PrescriptionListView.as_view(), name='prescription-list'),
    path('<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('patients/<int:patient_id>/', PatientPrescriptionsView.as_view(), name='patient-prescriptions'),
]