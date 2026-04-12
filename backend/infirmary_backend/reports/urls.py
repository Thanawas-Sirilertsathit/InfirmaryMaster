from django.urls import path
from .views import TriggerLowStockView, TriggerExpirationView, ReportsStatusView, NotificationListView, NotificationReadView

urlpatterns = [
    path('low-stock/', TriggerLowStockView.as_view(), name='trigger-low-stock'),
    path('expiration/', TriggerExpirationView.as_view(), name='trigger-expiration'),
    path('status/', ReportsStatusView.as_view(), name='reports-status'),
    path('notifications/', NotificationListView.as_view(), name='report-notification-list'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='report-notification-read'),
]