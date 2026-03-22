from django.db import models


class MedicineCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    category = models.ForeignKey(MedicineCategory, on_delete=models.PROTECT, related_name='medicines')
    name = models.CharField(max_length=128)
    dosage = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    minimum_stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'dosage')

    def __str__(self):
        return f"{self.name} ({self.dosage})"
