from django.urls import path
from .views import PatientCreateView, PatientSearchView, PatientDetailView, PatientPrescriptionsView

urlpatterns = [
    path('', PatientCreateView.as_view(), name='patient-create'),
    path('search/', PatientSearchView.as_view(), name='patient-search'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:patient_id>/prescriptions/', PatientPrescriptionsView.as_view(), name='patient-prescriptions'),
]