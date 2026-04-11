from django.db import models
from django.utils import timezone
from medicines.models import Medicine
import uuid
import logging

logger = logging.getLogger(__name__)


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


def deduct_stock(batch_id, quantity, reference='prescription'):
    logger.debug('Deducting stock for batch ID: %s, quantity: %d', batch_id, quantity)  # Log batch ID and quantity
    if quantity <= 0:
        return 0

    try:
        batch = MedicineBatch.objects.get(id=batch_id, expiration_date__gte=timezone.now().date())
    except MedicineBatch.DoesNotExist:
        logger.error('Batch ID %s does not exist or is expired', batch_id)  # Log error
        raise ValueError(f"Batch ID {batch_id} does not exist or is expired")

    if batch.quantity < quantity:
        logger.error('Not enough stock for batch ID: %s. Needed: %d, available: %d', batch_id, quantity, batch.quantity)  # Log error
        raise ValueError(f"Not enough stock for {batch.medicine} [{batch.batch_number}]. Needed {quantity}, available {batch.quantity}")

    batch.quantity -= quantity
    batch.save(update_fields=['quantity'])

    StockTransaction.objects.create(
        batch=batch,
        transaction_type=StockTransaction.TYPE_OUT,
        quantity=quantity,
        reference=reference,
        notes=f'Removed for {reference}',
    )

    return quantity
