#!/usr/bin/env python
"""
Setup admin permissions and groups for healthcare management system
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User

def setup_admin_permissions():
    """Set up admin groups and permissions"""
    
    # Create admin group if it doesn't exist
    admin_group, created = Group.objects.get_or_create(name='Administrators')
    if created:
        print("✅ Created 'Administrators' group")
    else:
        print("ℹ️  'Administrators' group already exists")
    
    # Get all permissions
    all_permissions = Permission.objects.all()
    
    # Add all permissions to admin group
    admin_group.permissions.set(all_permissions)
    admin_group.save()
    print(f"✅ Added {all_permissions.count()} permissions to Administrators group")
    
    # Add superuser to admin group
    try:
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            superuser.groups.add(admin_group)
            print(f"✅ Added superuser '{superuser.email}' to Administrators group")
        else:
            print("⚠️  No superuser found")
    except Exception as e:
        print(f"❌ Error adding superuser to group: {e}")
    
    print("\n=== Admin Setup Complete ===")
    print("Admin can now:")
    print("- Access Django admin at /admin/")
    print("- Manage all users, doctors, patients")
    print("- Monitor appointments and chat messages")
    print("- Perform system administration tasks")

def show_admin_stats():
    """Show current admin statistics"""
    print("\n=== Current System Statistics ===")
    
    from doctors.models import Doctor
    from patients.models import Patient
    from appointments.models import Appointment
    from chat.models import ChatRoom, Message
    
    print(f"Total Users: {User.objects.count()}")
    print(f"Superusers: {User.objects.filter(is_superuser=True).count()}")
    print(f"Staff Users: {User.objects.filter(is_staff=True).count()}")
    print(f"Doctors: {Doctor.objects.count()}")
    print(f"Patients: {Patient.objects.count()}")
    print(f"Appointments: {Appointment.objects.count()}")
    print(f"Chat Rooms: {ChatRoom.objects.count()}")
    print(f"Messages: {Message.objects.count()}")
    
    # Show recent activity
    print("\n=== Recent Activity ===")
    recent_appointments = Appointment.objects.order_by('-created_at')[:5]
    for apt in recent_appointments:
        print(f"- Appointment: {apt.patient.user.get_full_name()} with {apt.doctor.user.get_full_name()} on {apt.appointment_date}")
    
    recent_messages = Message.objects.order_by('-timestamp')[:5]
    for msg in recent_messages:
        sender_role = "Doctor" if msg.sender.groups.filter(name='Doctors').exists() else "Patient"
        print(f"- Message: {sender_role} {msg.sender.get_full_name()} - {msg.content[:30]}...")

if __name__ == "__main__":
    setup_admin_permissions()
    show_admin_stats()