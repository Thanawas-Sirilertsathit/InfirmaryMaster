from django.db import models
from django.conf import settings
from medicines.models import Medicine


class Prescription(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='issued_prescriptions')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription {self.id} for {self.patient}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='prescription_items')
    quantity = models.PositiveIntegerField()
    instruction = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('prescription', 'medicine')

    def __str__(self):
        return f"{self.quantity} x {self.medicine}"
