from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_low_stock_alert, send_expiration_alert
from users.permissions import IsStaffOrAdmin


class TriggerLowStockView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def post(self, request):
        count = send_low_stock_alert()
        return Response({
            'message': f'Low stock alert sent to {count} items'
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