#!/usr/bin/env python
"""
Database setup and migration script for healthcare management system
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

def test_database_connection():
    """Test PostgreSQL database connection"""
    print("🔍 Testing database connection...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def run_migrations():
    """Run Django migrations in correct order"""
    print("\n🔄 Running migrations...")
    try:
        from django.core.management import call_command
        
        # First, make migrations for accounts (custom user model)
        print("Creating accounts migrations...")
        call_command('makemigrations', 'accounts', verbosity=1)
        
        # Then other apps
        print("Creating other app migrations...")
        call_command('makemigrations', 'patients', 'doctors', 'appointments', 'chat', verbosity=1)
        
        # Run all migrations
        print("Applying migrations...")
        call_command('migrate', verbosity=1)
        
        print("✅ All migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_initial_data():
    """Create initial admin user and sample data"""
    print("\n👤 Creating initial data...")
    try:
        from accounts.models import User
        from patients.models import Patient
        from doctors.models import Doctor
        
        # Create superuser admin
        if not User.objects.filter(email='admin@healthcare.com').exists():
            admin = User.objects.create_user(
                email='admin@healthcare.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                role='admin',
                is_staff=True,
                is_superuser=True,
                phone_number='+1234567890'
            )
            print("✅ Admin user created: admin@healthcare.com / admin123")
        
        # Create sample doctor
        if not User.objects.filter(email='dr.smith@healthcare.com').exists():
            doctor_user = User.objects.create_user(
                email='dr.smith@healthcare.com',
                password='doctor123',
                first_name='John',
                last_name='Smith',
                role='doctor',
                phone_number='+1234567891'
            )
            
            Doctor.objects.create(
                user=doctor_user,
                specialization='general_medicine',
                license_number='MD12345',
                years_of_experience=10,
                education='MD from Medical University',
                bio='Experienced general practitioner with 10 years of practice.',
                consultation_fee=150.00,
                available_from='09:00',
                available_to='17:00',
                hospital_affiliation='City General Hospital',
                languages_spoken='English, Spanish',
                is_available=True
            )
            print("✅ Doctor created: dr.smith@healthcare.com / doctor123")
        
        # Create sample patient
        if not User.objects.filter(email='patient@healthcare.com').exists():
            patient_user = User.objects.create_user(
                email='patient@healthcare.com',
                password='patient123',
                first_name='Jane',
                last_name='Doe',
                role='patient',
                phone_number='+1234567892',
                date_of_birth='1990-01-01'
            )
            
            Patient.objects.create(
                user=patient_user,
                gender='F',
                blood_group='A+',
                height=165.0,
                weight=60.0,
                emergency_contact_name='John Doe',
                emergency_contact_phone='+1234567893',
                medical_history='No significant medical history',
                allergies='None known'
            )
            print("✅ Patient created: patient@healthcare.com / patient123")
        
        # Create general user
        if not User.objects.filter(email='user@healthcare.com').exists():
            User.objects.create_user(
                email='user@healthcare.com',
                password='user123',
                first_name='General',
                last_name='User',
                role='user',
                phone_number='+1234567894'
            )
            print("✅ General user created: user@healthcare.com / user123")
        
        return True
    except Exception as e:
        print(f"❌ Data creation error: {e}")
        return False

def verify_setup():
    """Verify the setup is working"""
    print("\n🔍 Verifying setup...")
    try:
        from accounts.models import User
        from patients.models import Patient
        from doctors.models import Doctor
        
        user_count = User.objects.count()
        patient_count = Patient.objects.count()
        doctor_count = Doctor.objects.count()
        
        print(f"✅ Total users: {user_count}")
        print(f"✅ Total patients: {patient_count}")
        print(f"✅ Total doctors: {doctor_count}")
        
        return True
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    print("🏥 Healthcare Management System - Database Setup")
    print("=" * 60)
    
    # Test database connection
    if not test_database_connection():
        print("\n💡 Database connection tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your .env file database credentials")
        print("3. Ensure the database 'healthcare_db' exists")
        print("4. Verify PostgreSQL is accepting connections on localhost:5432")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Migration failed!")
        sys.exit(1)
    
    # Create initial data
    if not create_initial_data():
        print("❌ Data creation failed!")
        sys.exit(1)
    
    # Verify setup
    verify_setup()
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📋 Login Credentials:")
    print("┌─────────────────────────────────────────────┐")
    print("│ Admin:   admin@healthcare.com / admin123   │")
    print("│ Doctor:  dr.smith@healthcare.com / doctor123│")
    print("│ Patient: patient@healthcare.com / patient123│")
    print("│ User:    user@healthcare.com / user123     │")
    print("└─────────────────────────────────────────────┘")
    print("\n🚀 Ready to start:")
    print("   python manage.py runserver")
    print("\n🌐 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   Admin:    http://localhost:8000/admin")

if __name__ == "__main__":
    main()