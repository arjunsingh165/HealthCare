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
    print("✅ Django setup successful!")
    
    # Test database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Database connection successful: {version}")
    
    # Test user creation
    from accounts.models import User
    print(f"✅ User model accessible. Total users: {User.objects.count()}")
    
    # Test starting development server
    from django.core.management import execute_from_command_line
    print("🚀 Starting Django development server...")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()