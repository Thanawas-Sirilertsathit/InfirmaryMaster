from django.conf import settings
from django.db import models
import uuid


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    medical_record_number = models.CharField(max_length=64, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.medical_record_number:
            self.medical_record_number = self._generate_medical_record_number()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_medical_record_number(cls):
        while True:
            candidate = f"MRN-{uuid.uuid4().hex[:12].upper()}"
            if not cls.objects.filter(medical_record_number=candidate).exists():
                return candidate

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.medical_record_number})"
