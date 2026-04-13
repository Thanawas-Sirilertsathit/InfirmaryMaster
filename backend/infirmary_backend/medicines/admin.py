from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage', 'category', 'minimum_stock')
    list_filter = ('category',)
    search_fields = ('name', 'dosage')
