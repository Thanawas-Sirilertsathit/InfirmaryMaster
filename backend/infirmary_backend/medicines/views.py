from rest_framework import generics
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
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineDetailView(generics.RetrieveUpdateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsStaffOrAdmin]