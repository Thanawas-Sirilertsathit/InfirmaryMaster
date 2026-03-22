from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('patients/', include('patients.urls')),
    path('medicines/', include('medicines.urls')),
    path('inventory/', include('inventory.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('reports/', include('reports.urls')),
]