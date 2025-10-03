#!/usr/bin/env python
import os
import sys
import subprocess

def start_django_server():
    print("🏥 Healthcare Management System")
    print("=" * 40)
    
    # Change to project directory
    project_dir = r"c:\Users\singh\OneDrive\Desktop\CODING\healthcare_management"
    os.chdir(project_dir)
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Check if manage.py exists
    if not os.path.exists("manage.py"):
        print("❌ manage.py not found!")
        return False
    
    print("✅ manage.py found")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
    
    try:
        # Import Django and run server
        import django
        from django.core.management import execute_from_command_line
        
        print(f"🐍 Django version: {django.get_version()}")
        
        # Setup Django
        django.setup()
        print("✅ Django setup complete")
        
        print("🚀 Starting development server...")
        print("📝 Backend: http://localhost:8000")
        print("📝 Admin: http://localhost:8000/admin")
        print("📝 Press Ctrl+C to stop")
        print("-" * 40)
        
        # Start server
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_django_server()