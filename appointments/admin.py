from django.contrib import admin
from .models import Appointment, Review

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_type', 'status', 'created_at')
    list_filter = ('status', 'appointment_type', 'appointment_date', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'is_upcoming')
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_type', 'status')
        }),
        ('Visit Information', {
            'fields': ('reason_for_visit', 'symptoms')
        }),
        ('Medical Notes', {
            'fields': ('notes', 'prescription', 'follow_up_date'),
            'classes': ('collapse',)
        }),
        ('Status Information', {
            'fields': ('rejection_reason',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'is_upcoming'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Review Details', {
            'fields': ('appointment', 'patient', 'doctor', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )