#!/usr/bin/env python
"""
Quick test script to verify appointment booking functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

def test_appointment_system():
    print("=== TESTING APPOINTMENT BOOKING SYSTEM ===\n")
    
    # Test data
    print("1. Testing data availability...")
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    print(f"   - Found {doctors.count()} doctors")
    print(f"   - Found {patients.count()} patients")
    
    if doctors.count() == 0 or patients.count() == 0:
        print("   ❌ No test data found. Run 'python manage.py create_sample_data' first")
        return
    
    print("   ✅ Test data is available\n")
    
    # Test appointment creation
    print("2. Testing appointment creation...")
    try:
        doctor = doctors.first()
        patient = patients.first()
        
        # Create a test appointment
        future_date = timezone.now() + timedelta(days=1)
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=future_date,
            reason_for_visit="Test appointment",
            symptoms="Test symptoms",
            appointment_type="consultation",
            status="pending"
        )
        print(f"   ✅ Created appointment: {appointment}")
        print(f"   - Patient: {patient.user.get_full_name()}")
        print(f"   - Doctor: Dr. {doctor.user.get_full_name()}")
        print(f"   - Date: {appointment.appointment_date}")
        print(f"   - Status: {appointment.status}\n")
        
    except Exception as e:
        print(f"   ❌ Failed to create appointment: {e}\n")
        return
    
    # Test appointment approval
    print("3. Testing appointment approval...")
    try:
        appointment.status = 'accepted'
        appointment.save()
        print(f"   ✅ Appointment approved: {appointment.status}\n")
    except Exception as e:
        print(f"   ❌ Failed to approve appointment: {e}\n")
        return
    
    # Test appointment rejection
    print("4. Testing appointment rejection...")
    try:
        appointment.status = 'rejected'
        appointment.rejection_reason = "Test rejection"
        appointment.save()
        print(f"   ✅ Appointment rejected: {appointment.status}\n")
    except Exception as e:
        print(f"   ❌ Failed to reject appointment: {e}\n")
        return
    
    # Show existing appointments
    print("5. Current appointments in system:")
    all_appointments = Appointment.objects.all().order_by('-created_at')
    for apt in all_appointments[:5]:  # Show last 5
        print(f"   - {apt.patient.user.get_full_name()} → Dr. {apt.doctor.user.get_full_name()}")
        print(f"     Date: {apt.appointment_date.strftime('%Y-%m-%d %H:%M')}, Status: {apt.status}")
    
    print(f"\n   Total appointments: {all_appointments.count()}")
    
    print("\n=== TEST COMPLETED SUCCESSFULLY ===")
    print("\nLogin credentials to test in browser:")
    print("Patient: patient1@healthcare.com / patient123")
    print("Doctor: dr.smith@healthcare.com / doctor123")
    print("Admin: admin@healthcare.com / admin123")
    print("\nServer URL: http://127.0.0.1:8000/")

if __name__ == "__main__":
    test_appointment_system()