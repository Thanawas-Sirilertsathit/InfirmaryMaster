from django.db import models


class MedicineCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    category = models.CharField(max_length=128)  # Changed to CharField
    name = models.CharField(max_length=128)
    dosage = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    minimum_stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('name', 'dosage')

    def __str__(self):
        return f"{self.name} ({self.dosage})"
