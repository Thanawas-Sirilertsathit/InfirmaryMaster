from rest_framework import generics
from django.db.models import Q
from .models import Medicine, MedicineCategory
from .serializers import MedicineSerializer, MedicineCategorySerializer
from users.permissions import IsStaffOrAdmin


class MedicineCategoryCreateView(generics.CreateAPIView):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [IsStaffOrAdmin]


class MedicineCategoryListView(generics.ListAPIView):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer


class MedicineCreateView(generics.CreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsStaffOrAdmin]


class MedicineListView(generics.ListAPIView):
    serializer_class = MedicineSerializer

    def get_queryset(self):
        queryset = Medicine.objects.all().order_by('name', 'dosage')
        search = self.request.query_params.get('search', '').strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset


class MedicineDetailView(generics.RetrieveUpdateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsStaffOrAdmin]