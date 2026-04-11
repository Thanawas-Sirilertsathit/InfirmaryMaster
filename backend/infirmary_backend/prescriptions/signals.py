from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PrescriptionItem


@receiver(post_save, sender=PrescriptionItem)
def handle_prescription_item_created(sender, instance, created, **kwargs):
    return None
