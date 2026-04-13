from django.urls import path
from .views import MedicineCreateView, MedicineListView, MedicineDetailView

urlpatterns = [
    path('', MedicineCreateView.as_view(), name='medicine-create'),
    path('list/', MedicineListView.as_view(), name='medicine-list'),
    path('<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),
]