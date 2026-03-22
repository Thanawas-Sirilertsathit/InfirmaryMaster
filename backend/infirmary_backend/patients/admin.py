from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('medical_record_number', 'user', 'date_of_birth')
    search_fields = ('medical_record_number', 'user__username', 'user__email')
