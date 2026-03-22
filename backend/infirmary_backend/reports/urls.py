from django.urls import path
from .views import TriggerLowStockView, TriggerExpirationView, ReportsStatusView

urlpatterns = [
    path('low-stock/', TriggerLowStockView.as_view(), name='trigger-low-stock'),
    path('expiration/', TriggerExpirationView.as_view(), name='trigger-expiration'),
    path('status/', ReportsStatusView.as_view(), name='reports-status'),
]