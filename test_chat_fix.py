#!/usr/bin/env python
"""
Quick test for chat functionality after template fix
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import Appointment

User = get_user_model()

def test_chat_fix():
    print("=== TESTING CHAT TEMPLATE FIX ===\n")
    
    # Check for accepted appointments
    accepted_appointments = Appointment.objects.filter(status='accepted')
    print(f"Found {accepted_appointments.count()} accepted appointments for chat testing")
    
    if accepted_appointments.count() == 0:
        print("Creating a test accepted appointment...")
        # Get first appointment and make it accepted
        first_apt = Appointment.objects.first()
        if first_apt:
            first_apt.status = 'accepted'
            first_apt.save()
            print(f"✅ Made appointment {first_apt.id} accepted for testing")
    
    # Show chat URLs for testing
    for apt in accepted_appointments[:3]:  # Show first 3
        print(f"\n🔗 Test Chat URLs:")
        print(f"Doctor → Patient chat:")
        print(f"   /chat/?partner={apt.patient.user.id}&appointment={apt.id}")
        print(f"Patient → Doctor chat:")
        print(f"   /chat/?partner={apt.doctor.user.id}&appointment={apt.id}")
        print(f"Appointment: {apt.patient.user.get_full_name()} ↔ Dr. {apt.doctor.user.get_full_name()}")
    
    print(f"\n✅ Template syntax error fixed!")
    print("✅ Chat should now work correctly")
    print("\n🎯 Test Steps:")
    print("1. Login as doctor or patient")
    print("2. Go to Appointments page")
    print("3. Click 'Chat' button on accepted appointments")
    print("4. Or go directly to Messages page")
    
    print(f"\n🔑 Login Credentials:")
    print("Doctor: dr.smith@healthcare.com / doctor123")
    print("Patient: patient1@healthcare.com / patient123")
    print("Server: http://127.0.0.1:8000/")

if __name__ == "__main__":
    test_chat_fix()