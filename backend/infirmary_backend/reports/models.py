from django.db import models
from django.utils import timezone


class ReportNotification(models.Model):
    TYPE_LOW_STOCK = 'low_stock'
    TYPE_OUT_OF_STOCK = 'out_of_stock'
    TYPE_EXPIRING_BATCH = 'expiring_batch'

    TYPE_CHOICES = [
        (TYPE_LOW_STOCK, 'Low Stock'),
        (TYPE_OUT_OF_STOCK, 'Out Of Stock'),
        (TYPE_EXPIRING_BATCH, 'Expiring Batch'),
    ]

    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    medicine = models.ForeignKey(
        'medicines.Medicine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='report_notifications',
    )
    batch = models.ForeignKey(
        'inventory.MedicineBatch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='report_notifications',
    )
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_read', '-created_at']

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at', 'updated_at'])

    def __str__(self):
        return f'{self.get_type_display()}: {self.title}'