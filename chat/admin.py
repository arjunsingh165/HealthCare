from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient', 'doctor', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 
                    'doctor__first_name', 'doctor__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Chat Room Details', {
            'fields': ('appointment', 'patient', 'doctor', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'sender', 'message_type', 'content_preview', 'is_read', 'timestamp')
    list_filter = ('message_type', 'is_read', 'timestamp')
    search_fields = ('sender__first_name', 'sender__last_name', 'content')
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('chat_room', 'sender', 'message_type', 'content')
        }),
        ('Attachments', {
            'fields': ('file_attachment', 'image_attachment'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'timestamp'),
            'classes': ('collapse',)
        }),
    )