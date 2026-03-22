from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import MedicineBatch, get_available_stock
from .serializers import MedicineBatchSerializer, InventorySummarySerializer
from users.permissions import IsStaffOrAdmin
from medicines.models import Medicine


class MedicineBatchCreateView(generics.CreateAPIView):
    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer
    permission_classes = [IsStaffOrAdmin]


class MedicineBatchUpdateView(generics.UpdateAPIView):
    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer
    permission_classes = [IsStaffOrAdmin]


class MedicineBatchDeleteView(generics.DestroyAPIView):
    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer
    permission_classes = [IsStaffOrAdmin]


class MedicineBatchListView(generics.ListAPIView):
    serializer_class = MedicineBatchSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        medicine_id = self.request.query_params.get('medicine')
        if medicine_id:
            return MedicineBatch.objects.filter(medicine_id=medicine_id)
        return MedicineBatch.objects.all()


class InventorySummaryView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        medicines = Medicine.objects.all()
        summary_data = []

        for medicine in medicines:
            total_stock = get_available_stock(medicine)
            now = timezone.now().date()
            soon_threshold = now + timedelta(days=30)
            later_threshold = now + timedelta(days=60)

            expiring_soon = MedicineBatch.objects.filter(
                medicine=medicine,
                expiration_date__lte=soon_threshold,
                expiration_date__gt=now
            ).aggregate(total=Sum('quantity'))['total'] or 0

            expiring_later = MedicineBatch.objects.filter(
                medicine=medicine,
                expiration_date__lte=later_threshold,
                expiration_date__gt=soon_threshold
            ).aggregate(total=Sum('quantity'))['total'] or 0

            summary_data.append({
                'medicine_id': medicine.id,
                'medicine_name': f"{medicine.name} ({medicine.dosage})",
                'total_stock': total_stock,
                'expiring_soon': expiring_soon,
                'expiring_later': expiring_later,
            })

        serializer = InventorySummarySerializer(summary_data, many=True)
        return Response({'data': serializer.data})