from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'blood_group', 'height', 'weight', 'bmi', 'created_at')
    list_filter = ('gender', 'blood_group', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'emergency_contact_name')
    readonly_fields = ('created_at', 'updated_at', 'bmi')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('gender', 'blood_group', 'height', 'weight')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'current_medications', 'allergies', 'symptoms', 'problems')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Insurance', {
            'fields': ('insurance_number',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
