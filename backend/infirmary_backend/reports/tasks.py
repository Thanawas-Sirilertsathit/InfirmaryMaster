from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from medicines.models import Medicine
from inventory.models import MedicineBatch, get_available_stock

from .models import ReportNotification


def _upsert_notification(notification_type, title, message, medicine=None, batch=None):
    notification = ReportNotification.objects.filter(
        type=notification_type,
        medicine=medicine,
        batch=batch,
        is_active=True,
    ).first()

    if notification:
        ReportNotification.objects.filter(pk=notification.pk).update(
            title=title,
            message=message,
        )
        return None

    return ReportNotification.objects.create(
        type=notification_type,
        title=title,
        message=message,
        medicine=medicine,
        batch=batch,
    )


def sync_inventory_notifications():
    active_low_stock_medicine_ids = []
    active_out_of_stock_medicine_ids = []
    created_notifications = []

    for medicine in Medicine.objects.all():
        stock = get_available_stock(medicine)

        if stock == 0:
            active_out_of_stock_medicine_ids.append(medicine.id)
            title = f'Out of stock: {medicine.name}'
            message = (
                f'{medicine.name} {medicine.dosage} is out of stock. '
                'Please restock this medicine.'
            )

            notification = _upsert_notification(
                ReportNotification.TYPE_OUT_OF_STOCK,
                title,
                message,
                medicine=medicine,
            )
            if notification:
                created_notifications.append(notification)

            continue

        if stock > medicine.minimum_stock:
            continue

        active_low_stock_medicine_ids.append(medicine.id)
        title = f'Low stock: {medicine.name}'
        message = (
            f'{medicine.name} {medicine.dosage} has {stock} units available. '
            f'Minimum stock is {medicine.minimum_stock}.'
        )

        notification = _upsert_notification(
            ReportNotification.TYPE_LOW_STOCK,
            title,
            message,
            medicine=medicine,
        )
        if notification:
            created_notifications.append(notification)

    ReportNotification.objects.filter(
        type=ReportNotification.TYPE_LOW_STOCK,
        is_active=True,
    ).exclude(medicine_id__in=active_low_stock_medicine_ids).update(
        is_active=False
    )

    ReportNotification.objects.filter(
        type=ReportNotification.TYPE_OUT_OF_STOCK,
        is_active=True,
    ).exclude(medicine_id__in=active_out_of_stock_medicine_ids).update(
        is_active=False
    )

    return created_notifications


def sync_low_stock_notifications():
    return sync_inventory_notifications()


def sync_expiration_notifications(days=30):
    threshold = timezone.now().date() + timedelta(days=days)
    expiring_batches = MedicineBatch.objects.filter(
        expiration_date__lte=threshold,
        quantity__gt=0,
    ).select_related('medicine')
    active_batch_ids = []
    created_notifications = []

    for batch in expiring_batches:
        active_batch_ids.append(batch.id)
        title = f'Expiring soon: {batch.medicine.name}'
        message = (
            f'Batch {batch.batch_number} of {batch.medicine.name} '
            f'({batch.medicine.dosage}) expires on {batch.expiration_date}.'
        )

        notification = _upsert_notification(
            ReportNotification.TYPE_EXPIRING_BATCH,
            title,
            message,
            medicine=batch.medicine,
            batch=batch,
        )
        if notification:
            created_notifications.append(notification)

    ReportNotification.objects.filter(
        type=ReportNotification.TYPE_EXPIRING_BATCH,
        is_active=True,
    ).exclude(batch_id__in=active_batch_ids).update(is_active=False)

    return created_notifications


def sync_report_notifications():
    low_stock_notifications = sync_inventory_notifications()
    expiration_notifications = sync_expiration_notifications()
    return low_stock_notifications + expiration_notifications


def send_low_stock_alert():
    low_stock_notifications = sync_inventory_notifications()
    if not low_stock_notifications:
        return 0

    body_lines = ['Inventory alert:']
    for notification in low_stock_notifications:
        body_lines.append(f'- {notification.message}')

    send_mail(
        subject='InfirmaryMaster Inventory Alert',
        message='\n'.join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.NOTIFICATION_EMAIL],
        fail_silently=False,
    )
    return len(low_stock_notifications)


def send_expiration_alert(days=30):
    expiring_notifications = sync_expiration_notifications(days=days)
    if not expiring_notifications:
        return 0

    body_lines = [f'Batches expiring in {days} days or less:']
    for notification in expiring_notifications:
        body_lines.append(f'- {notification.message}')

    send_mail(
        subject='InfirmaryMaster Expiration Alert',
        message='\n'.join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.NOTIFICATION_EMAIL],
        fail_silently=False,
    )
    return len(expiring_notifications)
