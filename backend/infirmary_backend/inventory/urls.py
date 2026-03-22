from django.urls import path
from .views import MedicineBatchCreateView, MedicineBatchUpdateView, MedicineBatchDeleteView, MedicineBatchListView, InventorySummaryView

urlpatterns = [
    path('batches/', MedicineBatchCreateView.as_view(), name='batch-create'),
    path('batches/<int:pk>/', MedicineBatchUpdateView.as_view(), name='batch-update'),
    path('batches/<int:pk>/delete/', MedicineBatchDeleteView.as_view(), name='batch-delete'),
    path('batches/list/', MedicineBatchListView.as_view(), name='batch-list'),
    path('summary/', InventorySummaryView.as_view(), name='inventory-summary'),
]