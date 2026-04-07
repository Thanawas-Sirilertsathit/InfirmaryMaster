from django.db import models
from django.utils import timezone
from medicines.models import Medicine
import uuid


class MedicineBatch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=64, unique=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField()
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.batch_number:
            self.batch_number = str(uuid.uuid4())[:8]  # Generate a unique 8-character batch number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine} [{self.batch_number}]"


class StockTransaction(models.Model):
    TYPE_IN = 'IN'
    TYPE_OUT = 'OUT'

    TRANSACTION_TYPE_CHOICES = [
        (TYPE_IN, 'Stock In'),
        (TYPE_OUT, 'Stock Out'),
    ]

    batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    reference = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.batch}"


def get_available_stock(medicine):
    batches = MedicineBatch.objects.filter(medicine=medicine)
    return sum(b.quantity for b in batches)


def deduct_stock(medicine, quantity, reference='prescription'):
    if quantity <= 0:
        return 0

    batches = MedicineBatch.objects.filter(medicine=medicine, expiration_date__gte=timezone.now().date()).order_by('expiration_date')
    remaining = quantity

    for batch in batches:
        if remaining <= 0:
            break

        take = min(batch.quantity, remaining)
        batch.quantity -= take
        batch.save(update_fields=['quantity'])

        StockTransaction.objects.create(
            batch=batch,
            transaction_type=StockTransaction.TYPE_OUT,
            quantity=take,
            reference=reference,
            notes=f'Removed for {reference}',
        )
        remaining -= take

    if remaining > 0:
        raise ValueError(f"Not enough stock for {medicine}. Needed {quantity}, available {quantity-remaining}")

    return quantity - remaining
