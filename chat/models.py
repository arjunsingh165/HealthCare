from django.db import models
from accounts.models import User
from appointments.models import Appointment

class ChatRoom(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='chat_room')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_chats')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_chats')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Chat: {self.patient.full_name} <-> Dr. {self.doctor.full_name} (Apt: {self.appointment.id})"


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    )
    
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True)
    file_attachment = models.FileField(upload_to='chat_files/', null=True, blank=True)
    image_attachment = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}..."
    
    @property
    def content_preview(self):
        """Return a preview of the message content"""
        if self.message_type == 'text':
            return self.content[:50] + '...' if len(self.content) > 50 else self.content
        elif self.message_type == 'image':
            return 'Image attachment'
        elif self.message_type == 'file':
            return 'File attachment'
        return 'Message'