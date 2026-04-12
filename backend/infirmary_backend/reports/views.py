from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ReportNotification
from .serializers import ReportNotificationSerializer
from .tasks import send_low_stock_alert, send_expiration_alert, sync_report_notifications
from users.permissions import IsStaffOrAdmin


class TriggerLowStockView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def post(self, request):
        count = send_low_stock_alert()
        return Response({
            'message': f'Inventory alert sent for {count} medicines'
        })


class TriggerExpirationView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def post(self, request):
        count = send_expiration_alert()
        return Response({
            'message': f'Expiration alert sent for {count} batches'
        })


class ReportsStatusView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        # For now, just return a placeholder. In production, track last run times.
        return Response({
            'last_low_stock_check': 'Not implemented yet',
            'last_expiration_check': 'Not implemented yet'
        })


class NotificationListView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        sync_report_notifications()
        notifications = ReportNotification.objects.filter(is_active=True)
        serializer = ReportNotificationSerializer(notifications, many=True)
        unread_count = notifications.filter(is_read=False).count()
        return Response({
            'unread_count': unread_count,
            'results': serializer.data,
        })


class NotificationReadView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def post(self, request, pk):
        try:
            notification = ReportNotification.objects.get(pk=pk, is_active=True)
        except ReportNotification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save(update_fields=['is_read', 'read_at', 'updated_at'])

        return Response({'message': 'Notification marked as read.'})