#!/usr/bin/env python
"""
Test chat functionality
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from accounts.models import User
from chat.models import ChatRoom, Message
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor

def test_chat_functionality():
    print("=== Testing Chat Functionality ===\n")
    
    # Get existing appointments
    accepted_appointments = Appointment.objects.filter(status='accepted')
    print(f"Accepted appointments: {accepted_appointments.count()}")
    
    for apt in accepted_appointments[:3]:  # Test first 3 appointments
        print(f"\nTesting appointment: {apt.patient.user.get_full_name()} with {apt.doctor.user.get_full_name()}")
        
        # Get or create chat room
        chat_room, created = ChatRoom.objects.get_or_create(
            appointment=apt,
            defaults={
                'patient': apt.patient.user,
                'doctor': apt.doctor.user,
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created new chat room for appointment {apt.id}")
        else:
            print(f"ℹ️  Chat room already exists for appointment {apt.id}")
        
        # Check existing messages
        existing_messages = Message.objects.filter(chat_room=chat_room).count()
        print(f"   Existing messages: {existing_messages}")
        
        # Create test messages if none exist
        if existing_messages == 0:
            # Patient message
            Message.objects.create(
                chat_room=chat_room,
                sender=apt.patient.user,
                content=f"Hello Dr. {apt.doctor.user.get_full_name()}, I have some questions about my appointment.",
                message_type='text'
            )
            
            # Doctor reply
            Message.objects.create(
                chat_room=chat_room,
                sender=apt.doctor.user,
                content=f"Hello {apt.patient.user.get_full_name()}, I'm happy to help. What questions do you have?",
                message_type='text'
            )
            
            print(f"✅ Created test messages for this chat room")
        
        # Test message retrieval
        messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
        print(f"   Total messages now: {messages.count()}")
        
        for msg in messages:
            sender_role = "Doctor" if msg.sender.groups.filter(name='Doctors').exists() else "Patient"
            print(f"   - {sender_role} ({msg.sender.get_full_name()}): {msg.content[:50]}...")
    
    print(f"\n=== Chat System Summary ===")
    print(f"Total Chat Rooms: {ChatRoom.objects.count()}")
    print(f"Total Messages: {Message.objects.count()}")
    print(f"Active Chat Rooms: {ChatRoom.objects.filter(is_active=True).count()}")
    
    # Test access for different users
    print(f"\n=== Testing User Access ===")
    for user in User.objects.filter(role__in=['patient', 'doctor'])[:3]:
        if user.role == 'patient':
            try:
                patient = Patient.objects.get(user=user)
                accessible_chats = ChatRoom.objects.filter(patient=user)
                print(f"Patient {user.get_full_name()}: {accessible_chats.count()} accessible chats")
            except Patient.DoesNotExist:
                print(f"Patient {user.get_full_name()}: No patient profile")
        
        elif user.role == 'doctor':
            try:
                doctor = Doctor.objects.get(user=user)
                accessible_chats = ChatRoom.objects.filter(doctor=user)
                print(f"Doctor {user.get_full_name()}: {accessible_chats.count()} accessible chats")
            except Doctor.DoesNotExist:
                print(f"Doctor {user.get_full_name()}: No doctor profile")

if __name__ == "__main__":
    test_chat_functionality()