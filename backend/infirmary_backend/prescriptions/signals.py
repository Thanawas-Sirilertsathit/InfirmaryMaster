from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PrescriptionItem
from inventory.models import deduct_stock


@receiver(post_save, sender=PrescriptionItem)
def handle_prescription_item_created(sender, instance, created, **kwargs):
    if not created:
        return

    # Deduct stock immediately when a new prescription item is added
    try:
        deducted = deduct_stock(instance.medicine, instance.quantity, reference=f'Prescription {instance.prescription.id}')
    except Exception as exc:
        # in production, there should be a better retry/log handling
        raise

    return deducted
