from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment, Review
from datetime import datetime, timedelta
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for healthcare management system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new sample data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Appointment.objects.all().delete()
            Doctor.objects.all().delete()
            Patient.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating sample users...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@healthcare.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone_number': '+1234567890',
                'address': '123 Admin St, Admin City'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.email}')

        # Create doctor users
        doctor_data = [
            {
                'email': 'dr.smith@healthcare.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'specialization': 'cardiology',
                'license_number': 'MD001',
                'years_of_experience': 15,
                'consultation_fee': 200.00,
                'bio': 'Experienced cardiologist with 15 years of practice.',
                'hospital_affiliation': 'City General Hospital',
                'available_from': '09:00',
                'available_to': '17:00'
            },
            {
                'email': 'dr.johnson@healthcare.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'specialization': 'dermatology',
                'license_number': 'MD002',
                'years_of_experience': 10,
                'consultation_fee': 150.00,
                'bio': 'Dermatology specialist focusing on skin health.',
                'hospital_affiliation': 'Skin Care Center',
                'available_from': '10:00',
                'available_to': '18:00'
            },
            {
                'email': 'dr.brown@healthcare.com',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'specialization': 'general_medicine',
                'license_number': 'MD003',
                'years_of_experience': 8,
                'consultation_fee': 100.00,
                'bio': 'General practitioner providing comprehensive care.',
                'hospital_affiliation': 'Community Health Center',
                'available_from': '08:00',
                'available_to': '16:00'
            },
            {
                'email': 'dr.davis@healthcare.com',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'specialization': 'pediatrics',
                'license_number': 'MD004',
                'years_of_experience': 12,
                'consultation_fee': 180.00,
                'bio': 'Pediatrician specializing in child healthcare.',
                'hospital_affiliation': 'Children\'s Hospital',
                'available_from': '09:00',
                'available_to': '17:00'
            }
        ]

        doctors = []
        for data in doctor_data:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'doctor',
                    'phone_number': f'+123456{random.randint(1000, 9999)}',
                    'address': f'{random.randint(100, 999)} Medical St, Health City'
                }
            )
            if created:
                user.set_password('doctor123')
                user.save()
                self.stdout.write(f'Created doctor user: {user.email}')

            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': data['specialization'],
                    'license_number': data['license_number'],
                    'experience_years': data['years_of_experience'],
                    'consultation_fee': data['consultation_fee'],
                    'bio': data['bio'],
                    'hospital_affiliation': data['hospital_affiliation'],
                    'available_from': data['available_from'],
                    'available_to': data['available_to'],
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'total_reviews': random.randint(10, 50)
                }
            )
            if created:
                self.stdout.write(f'Created doctor profile: Dr. {user.full_name}')
            doctors.append(doctor)

        # Create patient users
        patient_data = [
            {
                'email': 'patient1@healthcare.com',
                'first_name': 'Alice',
                'last_name': 'Wilson',
                'gender': 'F',
                'blood_group': 'A+',
                'height': 165,
                'weight': 60
            },
            {
                'email': 'patient2@healthcare.com',
                'first_name': 'Bob',
                'last_name': 'Taylor',
                'gender': 'M',
                'blood_group': 'O+',
                'height': 175,
                'weight': 75
            },
            {
                'email': 'patient3@healthcare.com',
                'first_name': 'Carol',
                'last_name': 'Anderson',
                'gender': 'F',
                'blood_group': 'B+',
                'height': 160,
                'weight': 55
            }
        ]

        patients = []
        for data in patient_data:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'patient',
                    'phone_number': f'+123456{random.randint(1000, 9999)}',
                    'address': f'{random.randint(100, 999)} Patient St, Health City',
                    'date_of_birth': timezone.now().date() - timedelta(days=random.randint(20*365, 60*365))
                }
            )
            if created:
                user.set_password('patient123')
                user.save()
                self.stdout.write(f'Created patient user: {user.email}')

            patient, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'gender': data['gender'],
                    'blood_group': data['blood_group'],
                    'height': data['height'],
                    'weight': data['weight'],
                    'emergency_contact_name': f'Emergency Contact for {user.first_name}',
                    'emergency_contact_phone': f'+123456{random.randint(1000, 9999)}',
                    'medical_history': 'No significant medical history',
                    'allergies': 'None known'
                }
            )
            if created:
                self.stdout.write(f'Created patient profile: {user.full_name}')
            patients.append(patient)

        # Create general users
        general_users = [
            {
                'email': 'user1@healthcare.com',
                'first_name': 'General',
                'last_name': 'User1'
            },
            {
                'email': 'user2@healthcare.com',
                'first_name': 'General',
                'last_name': 'User2'
            }
        ]

        for data in general_users:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'user',
                    'phone_number': f'+123456{random.randint(1000, 9999)}',
                    'address': f'{random.randint(100, 999)} User St, Health City'
                }
            )
            if created:
                user.set_password('user123')
                user.save()
                self.stdout.write(f'Created general user: {user.email}')

        # Create sample appointments
        self.stdout.write('Creating sample appointments...')
        appointment_types = ['consultation', 'follow_up', 'checkup']
        
        for i in range(20):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            
            # Create appointments with various statuses and dates
            appointment_date = timezone.now() + timedelta(days=random.randint(-30, 30))
            status = random.choice(['pending', 'accepted', 'completed', 'rejected'])
            
            appointment, created = Appointment.objects.get_or_create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                defaults={
                    'appointment_type': random.choice(appointment_types),
                    'status': status,
                    'reason_for_visit': f'Sample appointment reason #{i+1}',
                    'symptoms': f'Sample symptoms #{i+1}' if random.choice([True, False]) else '',
                    'notes': f'Doctor notes #{i+1}' if status == 'completed' else '',
                    'prescription': f'Sample prescription #{i+1}' if status == 'completed' else ''
                }
            )
            
            if created:
                self.stdout.write(f'Created appointment: {patient.user.full_name} -> Dr. {doctor.user.full_name}')
                
                # Create reviews for completed appointments
                if status == 'completed' and random.choice([True, False]):
                    Review.objects.get_or_create(
                        appointment=appointment,
                        patient=patient,
                        doctor=doctor,
                        defaults={
                            'rating': random.randint(3, 5),
                            'comment': f'Great experience with Dr. {doctor.user.full_name}!'
                        }
                    )

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
        self.stdout.write('Use these credentials to test:')
        self.stdout.write('Admin: admin@healthcare.com / admin123')
        self.stdout.write('Doctor: dr.smith@healthcare.com / doctor123')
        self.stdout.write('Patient: patient1@healthcare.com / patient123')
        self.stdout.write('General User: user1@healthcare.com / user123')