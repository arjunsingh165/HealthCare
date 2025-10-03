#!/usr/bin/env python
import os
import sys
import django

# Add the project to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')

try:
    django.setup()
    print("🏥 Healthcare Management System - Clean Database Setup")
    print("=" * 60)
    
    # Test database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Database connection successful: {version}")
    
    # Clear existing data except superuser
    from accounts.models import User
    from patients.models import Patient
    from doctors.models import Doctor
    from appointments.models import Appointment
    from chat.models import ChatRoom, Message
    
    print("\n🧹 Cleaning existing demo data...")
    
    # Delete all non-superuser accounts
    User.objects.filter(is_superuser=False).delete()
    print("✅ Removed all demo accounts")
    
    # Clean related data
    Patient.objects.all().delete()
    Doctor.objects.all().delete()
    Appointment.objects.all().delete()
    ChatRoom.objects.all().delete()
    Message.objects.all().delete()
    print("✅ Cleaned all related data")
    
    # Create only superuser if it doesn't exist
    if not User.objects.filter(is_superuser=True).exists():
        admin_user = User.objects.create_superuser(
            email='admin@healthcare.com',
            password='admin123',
            first_name='Super',
            last_name='Admin',
            role='admin'
        )
        print("✅ Created superuser: admin@healthcare.com / admin123")
    else:
        print("✅ Superuser already exists")
    
    print(f"\n📊 Final Statistics:")
    print(f"✅ Total users: {User.objects.count()}")
    print(f"✅ Superusers: {User.objects.filter(is_superuser=True).count()}")
    print(f"✅ Patients: {Patient.objects.count()}")
    print(f"✅ Doctors: {Doctor.objects.count()}")
    
    print(f"\n🎉 Clean database setup completed!")
    print(f"\n📋 Access Information:")
    print("┌─────────────────────────────────────────────┐")
    print("│ Superuser: admin@healthcare.com / admin123 │")
    print("│ Users must register themselves             │")
    print("└─────────────────────────────────────────────┘")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()