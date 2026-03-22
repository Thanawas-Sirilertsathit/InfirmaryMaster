from django.core.management.base import BaseCommand
from reports.tasks import send_low_stock_alert, send_expiration_alert


class Command(BaseCommand):
    help = 'Send low stock and near-expiration alerts'

    def handle(self, *args, **options):
        low_count = send_low_stock_alert()
        exp_count = send_expiration_alert()

        self.stdout.write(self.style.SUCCESS(f'Low stock alerts sent: {low_count}'))
        self.stdout.write(self.style.SUCCESS(f'Expiration alerts sent: {exp_count}'))
