#!/usr/bin/env python
import os
import shutil

def cleanup_project():
    """Clean up unnecessary files and organize the project"""
    print("🧹 Cleaning up Healthcare Management System")
    print("=" * 50)
    
    project_dir = r"c:\Users\singh\OneDrive\Desktop\CODING\healthcare_management"
    os.chdir(project_dir)
    
    # Files and directories to remove
    cleanup_items = [
        'test_django.py',
        'test_api.py', 
        'start_server.ps1',
        'frontend_backup',  # if exists
        '__pycache__',
        '*.pyc',
        '.env',  # if exists and empty
    ]
    
    # Remove unnecessary files
    for item in cleanup_items:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"✅ Removed directory: {item}")
                else:
                    os.remove(item)
                    print(f"✅ Removed file: {item}")
            except Exception as e:
                print(f"⚠️  Could not remove {item}: {e}")
    
    # Remove __pycache__ directories recursively
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"✅ Removed: {dir_path}")
                except Exception as e:
                    print(f"⚠️  Could not remove {dir_path}: {e}")
    
    print("\n📋 Final Project Structure:")
    print("=" * 30)
    
    # Show clean project structure
    important_files = [
        'manage.py',
        'requirements.txt',
        'setup_database.py',
        'start_django.py',
        'healthcare_backend/',
        'accounts/',
        'patients/', 
        'doctors/',
        'appointments/',
        'chat/',
        'frontend/',
        'static/',
    ]
    
    for item in important_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"📁 {item}/")
            else:
                print(f"📄 {item}")
    
    print(f"\n🎉 Cleanup completed!")
    print(f"📂 Project directory: {os.getcwd()}")
    print(f"🚀 Ready to run: python start_django.py")

if __name__ == "__main__":
    cleanup_project()