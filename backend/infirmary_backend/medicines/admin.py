from django.contrib import admin
from .models import Medicine, MedicineCategory


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage', 'category', 'minimum_stock')
    list_filter = ('category',)
    search_fields = ('name', 'dosage')
