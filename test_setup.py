#!/usr/bin/env python
"""
Quick test script to verify Django setup and create initial data
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

def test_django_setup():
    print("🔍 Testing Django setup...")
    
    try:
        from django.core.management import execute_from_command_line
        print("✅ Django management commands available")
        
        # Test model imports
        from accounts.models import User
        from patients.models import Patient
        from doctors.models import Doctor
        from appointments.models import Appointment
        from chat.models import ChatRoom, Message
        print("✅ All models imported successfully")
        
        # Test settings
        from django.conf import settings
        print(f"✅ Settings loaded: {settings.DEBUG=}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_migrations():
    print("\n🔄 Running migrations...")
    try:
        from django.core.management import call_command
        
        # Make migrations
        call_command('makemigrations', verbosity=1)
        print("✅ Migrations created")
        
        # Run migrations
        call_command('migrate', verbosity=1)
        print("✅ Migrations applied")
        
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_superuser():
    print("\n👤 Creating superuser...")
    try:
        from accounts.models import User
        
        if not User.objects.filter(email='admin@healthcare.com').exists():
            admin = User.objects.create_user(
                email='admin@healthcare.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            print("✅ Superuser created: admin@healthcare.com / admin123")
        else:
            print("ℹ️  Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Superuser creation error: {e}")
        return False

def create_sample_users():
    print("\n📊 Creating sample users...")
    try:
        from accounts.models import User
        from patients.models import Patient
        from doctors.models import Doctor
        
        # Create doctor
        if not User.objects.filter(email='doctor@healthcare.com').exists():
            doctor_user = User.objects.create_user(
                email='doctor@healthcare.com',
                password='doctor123',
                first_name='John',
                last_name='Smith',
                role='doctor'
            )
            
            Doctor.objects.create(
                user=doctor_user,
                specialization='general_medicine',
                license_number='MD001',
                years_of_experience=10,
                consultation_fee=150.00,
                available_from='09:00',
                available_to='17:00'
            )
            print("✅ Doctor created: doctor@healthcare.com / doctor123")
        
        # Create patient
        if not User.objects.filter(email='patient@healthcare.com').exists():
            patient_user = User.objects.create_user(
                email='patient@healthcare.com',
                password='patient123',
                first_name='Jane',
                last_name='Doe',
                role='patient'
            )
            
            Patient.objects.create(
                user=patient_user,
                gender='F',
                blood_group='A+',
                height=165,
                weight=60
            )
            print("✅ Patient created: patient@healthcare.com / patient123")
        
        # Create general user
        if not User.objects.filter(email='user@healthcare.com').exists():
            User.objects.create_user(
                email='user@healthcare.com',
                password='user123',
                first_name='General',
                last_name='User',
                role='user'
            )
            print("✅ General user created: user@healthcare.com / user123")
        
        return True
    except Exception as e:
        print(f"❌ Sample user creation error: {e}")
        return False

def main():
    print("🏥 Healthcare Management System Test & Setup")
    print("=" * 50)
    
    if not test_django_setup():
        sys.exit(1)
    
    if not run_migrations():
        print("⚠️  Migration failed, but continuing...")
    
    if not create_superuser():
        print("⚠️  Superuser creation failed, but continuing...")
    
    if not create_sample_users():
        print("⚠️  Sample user creation failed, but continuing...")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Test Credentials:")
    print("Admin: admin@healthcare.com / admin123")
    print("Doctor: doctor@healthcare.com / doctor123")
    print("Patient: patient@healthcare.com / patient123")
    print("User: user@healthcare.com / user123")
    print("\n🚀 Start server: python manage.py runserver")

if __name__ == "__main__":
    main()