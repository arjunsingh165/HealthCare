#!/usr/bin/env python
"""
Create sample messages for real-time dashboard testing
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import Appointment
from chat.models import ChatRoom, Message
from django.utils import timezone
import random

User = get_user_model()

def create_sample_messages():
    print("=== CREATING SAMPLE MESSAGES FOR DASHBOARD TESTING ===\n")
    
    # Get accepted appointments
    accepted_appointments = Appointment.objects.filter(status='accepted')
    print(f"Found {accepted_appointments.count()} accepted appointments")
    
    if accepted_appointments.count() == 0:
        print("Creating accepted appointments...")
        # Make some appointments accepted
        pending_appointments = Appointment.objects.filter(status='pending')[:3]
        for apt in pending_appointments:
            apt.status = 'accepted'
            apt.save()
            print(f"✅ Made appointment {apt.id} accepted")
        
        accepted_appointments = Appointment.objects.filter(status='accepted')
    
    # Sample messages from doctors to patients
    doctor_messages = [
        "Hello! I've reviewed your medical history. How are you feeling today?",
        "Your test results look good. Let's schedule a follow-up appointment.",
        "Please remember to take your medication as prescribed.",
        "I've updated your treatment plan. You can view it in your patient portal.",
        "Thank you for your questions. Let me explain the diagnosis in detail.",
        "Your symptoms are improving. Keep following the treatment plan.",
        "I recommend some lifestyle changes we discussed during our appointment.",
        "Please monitor your blood pressure and report any unusual readings."
    ]
    
    # Sample messages from patients to doctors
    patient_messages = [
        "Thank you for the consultation, Doctor. I have a few follow-up questions.",
        "I'm experiencing some side effects from the medication. Should I be concerned?",
        "My symptoms have improved significantly since our last meeting.",
        "I've been following your advice and feeling much better.",
        "Could you please clarify the dosage for my evening medication?",
        "I'd like to schedule another appointment when you're available.",
        "The treatment is working well. Thank you for your care.",
        "I have some new symptoms I'd like to discuss with you."
    ]
    
    messages_created = 0
    
    for appointment in accepted_appointments[:5]:  # Create messages for first 5 appointments
        try:
            # Get or create chat room
            chat_room, created = ChatRoom.objects.get_or_create(
                appointment=appointment,
                patient=appointment.patient.user,
                doctor=appointment.doctor.user
            )
            
            if created:
                print(f"✅ Created chat room for {appointment.patient.user.get_full_name()} ↔ Dr. {appointment.doctor.user.get_full_name()}")
            
            # Create messages from doctor to patient
            doctor_message = Message.objects.create(
                chat_room=chat_room,
                sender=appointment.doctor.user,
                content=random.choice(doctor_messages),
                timestamp=timezone.now() - timezone.timedelta(minutes=random.randint(5, 60))
            )
            messages_created += 1
            print(f"📩 Doctor → Patient: {doctor_message.content[:50]}...")
            
            # Create messages from patient to doctor
            patient_message = Message.objects.create(
                chat_room=chat_room,
                sender=appointment.patient.user,
                content=random.choice(patient_messages),
                timestamp=timezone.now() - timezone.timedelta(minutes=random.randint(1, 30))
            )
            messages_created += 1
            print(f"📩 Patient → Doctor: {patient_message.content[:50]}...")
            
        except Exception as e:
            print(f"❌ Error creating messages for appointment {appointment.id}: {e}")
    
    print(f"\n✅ Created {messages_created} sample messages!")
    print("\n🎯 Test the Real-Time Dashboard:")
    print("1. Login as Patient → Check dashboard for doctor messages")
    print("2. Login as Doctor → Check dashboard for patient messages")
    print("3. Messages will appear in the 'Recent Messages' section")
    
    print(f"\n🔑 Login Credentials:")
    print("Patient: patient1@healthcare.com / patient123")
    print("Doctor: dr.smith@healthcare.com / doctor123")
    print("Server: http://127.0.0.1:8000/dashboard/")
    
    # Show some statistics
    total_messages = Message.objects.count()
    total_chat_rooms = ChatRoom.objects.count()
    print(f"\n📊 Chat Statistics:")
    print(f"Total Messages: {total_messages}")
    print(f"Total Chat Rooms: {total_chat_rooms}")
    print(f"Active Conversations: {ChatRoom.objects.filter(is_active=True).count()}")

if __name__ == "__main__":
    create_sample_messages()