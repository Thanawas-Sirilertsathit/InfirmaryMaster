from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import MedicineBatch


def schedule_report_notification_sync():
    from reports.tasks import sync_report_notifications

    transaction.on_commit(sync_report_notifications)


@receiver(post_save, sender=MedicineBatch)
def sync_reports_after_batch_save(sender, **kwargs):
    schedule_report_notification_sync()


@receiver(post_delete, sender=MedicineBatch)
def sync_reports_after_batch_delete(sender, **kwargs):
    schedule_report_notification_sync()