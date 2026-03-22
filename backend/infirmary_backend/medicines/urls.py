from django.urls import path
from .views import MedicineCategoryCreateView, MedicineCategoryListView, MedicineCreateView, MedicineListView, MedicineDetailView

urlpatterns = [
    path('categories/', MedicineCategoryCreateView.as_view(), name='category-create'),
    path('categories/list/', MedicineCategoryListView.as_view(), name='category-list'),
    path('', MedicineCreateView.as_view(), name='medicine-create'),
    path('list/', MedicineListView.as_view(), name='medicine-list'),
    path('<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),
]