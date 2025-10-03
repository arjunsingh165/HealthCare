#!/usr/bin/env python
"""
Test script to verify dashboard messaging functionality
This script will check if messages are correctly displayed on dashboards
"""

import os
import django
from django.core.management import setup_environ

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import ChatRoom, Message
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor

def test_dashboard_messages():
    print("=== Testing Dashboard Messaging Functionality ===\n")
    
    # Get existing users
    patients = User.objects.filter(groups__name='Patients')
    doctors = User.objects.filter(groups__name='Doctors')
    
    print(f"Total Patients: {patients.count()}")
    print(f"Total Doctors: {doctors.count()}")
    print(f"Total Chat Rooms: {ChatRoom.objects.count()}")
    print(f"Total Messages: {Message.objects.count()}\n")
    
    # Check messages for each patient
    print("=== Patient Dashboard Message Check ===")
    for patient_user in patients:
        try:
            patient = Patient.objects.get(user=patient_user)
            # Get messages from doctors (what patient should see)
            chat_rooms = ChatRoom.objects.filter(appointment__patient=patient)
            doctor_messages = Message.objects.filter(
                chat_room__in=chat_rooms,
                sender__groups__name='Doctors'
            ).order_by('-timestamp')[:5]
            
            print(f"Patient: {patient_user.get_full_name() or patient_user.username}")
            print(f"  - Chat Rooms: {chat_rooms.count()}")
            print(f"  - Messages from Doctors: {doctor_messages.count()}")
            
            for msg in doctor_messages:
                print(f"    • {msg.sender.get_full_name()}: {msg.content[:50]}...")
            print()
            
        except Patient.DoesNotExist:
            print(f"Patient profile not found for user: {patient_user.username}")
    
    # Check messages for each doctor
    print("=== Doctor Dashboard Message Check ===")
    for doctor_user in doctors:
        try:
            doctor = Doctor.objects.get(user=doctor_user)
            # Get messages from patients (what doctor should see)
            chat_rooms = ChatRoom.objects.filter(appointment__doctor=doctor)
            patient_messages = Message.objects.filter(
                chat_room__in=chat_rooms,
                sender__groups__name='Patients'
            ).order_by('-timestamp')[:5]
            
            print(f"Doctor: {doctor_user.get_full_name() or doctor_user.username}")
            print(f"  - Chat Rooms: {chat_rooms.count()}")
            print(f"  - Messages from Patients: {patient_messages.count()}")
            
            for msg in patient_messages:
                print(f"    • {msg.sender.get_full_name()}: {msg.content[:50]}...")
            print()
            
        except Doctor.DoesNotExist:
            print(f"Doctor profile not found for user: {doctor_user.username}")
    
    print("=== Recent Messages Summary ===")
    recent_messages = Message.objects.order_by('-timestamp')[:10]
    for msg in recent_messages:
        sender_role = "Doctor" if msg.sender.groups.filter(name='Doctors').exists() else "Patient"
        print(f"{msg.timestamp.strftime('%Y-%m-%d %H:%M')} - {sender_role} ({msg.sender.get_full_name()}): {msg.content[:30]}...")

if __name__ == "__main__":
    test_dashboard_messages()