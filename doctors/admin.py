from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'consultation_fee', 
                   'rating', 'is_available', 'created_at')
    list_filter = ('specialization', 'is_available', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 
                    'license_number', 'hospital_affiliation')
    readonly_fields = ('created_at', 'updated_at', 'rating', 'total_reviews')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Details', {
            'fields': ('specialization', 'license_number', 'experience_years', 
                      'education', 'bio')
        }),
        ('Practice Information', {
            'fields': ('consultation_fee', 'available_from', 'available_to', 
                      'is_available', 'hospital_affiliation', 'languages_spoken')
        }),
        ('Ratings', {
            'fields': ('rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
