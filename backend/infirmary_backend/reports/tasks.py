from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from medicines.models import Medicine
from inventory.models import MedicineBatch, get_available_stock


def send_low_stock_alert():
    low_stock_items = []
    for medicine in Medicine.objects.all():
        stock = get_available_stock(medicine)
        if stock <= medicine.minimum_stock:
            low_stock_items.append((medicine, stock))

    if not low_stock_items:
        return 0

    body_lines = ['Low stock alert:']
    for med, qty in low_stock_items:
        body_lines.append(f'- {med.name} {med.dosage}: {qty} units available, minimum {med.minimum_stock}')

    send_mail(
        subject='InfirmaryMaster Low Stock Alert',
        message='\n'.join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.NOTIFICATION_EMAIL],
        fail_silently=False,
    )
    return len(low_stock_items)


def send_expiration_alert(days=30):
    threshold = timezone.now().date() + timedelta(days=days)
    expiring_batches = MedicineBatch.objects.filter(expiration_date__lte=threshold)
    if not expiring_batches.exists():
        return 0

    body_lines = [f'Batches expiring in {days} days or less:']
    for batch in expiring_batches:
        body_lines.append(f'- {batch.medicine} batch {batch.batch_number} expires {batch.expiration_date}')

    send_mail(
        subject='InfirmaryMaster Expiration Alert',
        message='\n'.join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.NOTIFICATION_EMAIL],
        fail_silently=False,
    )
    return expiring_batches.count()
