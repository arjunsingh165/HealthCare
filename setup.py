#!/usr/bin/env python3
"""
Healthcare Management System Setup Script
Safe cross-platform setup using Python
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(command, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_requirements():
    """Check if required software is installed"""
    print("🔍 Checking system requirements...")
    
    # Check Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check Node.js
    success, output = run_command(["node", "--version"])
    if not success:
        print("❌ Node.js is not installed. Please install Node.js 16+")
        return False
    print(f"✅ Node.js {output.strip()}")
    
    # Check PostgreSQL (optional warning)
    success, _ = run_command(["psql", "--version"])
    if not success:
        print("⚠️  PostgreSQL not found. Please install PostgreSQL and configure database")
        print("   You can continue setup and configure the database later.")
    else:
        print("✅ PostgreSQL found")
    
    return True

def setup_backend():
    """Setup Django backend"""
    print("\n🐍 Setting up Django backend...")
    
    # Create virtual environment
    venv_path = Path("healthcare_env")
    if not venv_path.exists():
        print("Creating virtual environment...")
        success, _ = run_command([sys.executable, "-m", "venv", "healthcare_env"])
        if not success:
            print("❌ Failed to create virtual environment")
            return False
    
    # Determine activation script path
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate"
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Install requirements
    print("Installing Python dependencies...")
    success, _ = run_command([str(pip_exe), "install", "-r", "requirements.txt"])
    if not success:
        print("❌ Failed to install Python dependencies")
        return False
    
    # Create .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        env_example = Path(".env.example")
        if env_example.exists():
            shutil.copy(env_example, env_file)
        else:
            # Create basic .env file
            with open(env_file, 'w') as f:
                f.write("DJANGO_SECRET_KEY=django-insecure-change-this-in-production-123456789\n")
                f.write("DEBUG=True\n")
                f.write("POSTGRES_DB=healthcare_db\n")
                f.write("POSTGRES_USER=healthcare_user\n")
                f.write("POSTGRES_PASSWORD=healthcare_password\n")
                f.write("POSTGRES_HOST=localhost\n")
                f.write("POSTGRES_PORT=5432\n")
                f.write("ACCESS_TOKEN_LIFETIME_HOURS=24\n")
        print("⚠️  Please update the .env file with your database credentials")
    
    # Run migrations
    print("Running database migrations...")
    success, _ = run_command([str(python_exe), "manage.py", "makemigrations"])
    if not success:
        print("⚠️  Failed to create migrations - you may need to configure database first")
    
    success, _ = run_command([str(python_exe), "manage.py", "migrate"])
    if not success:
        print("⚠️  Failed to run migrations - you may need to configure database first")
    
    return True

def setup_frontend():
    """Setup React frontend"""
    print("\n⚛️  Setting up React frontend...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    os.chdir(frontend_path)
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    success, _ = run_command(["npm", "install"])
    if not success:
        print("❌ Failed to install Node.js dependencies")
        return False
    
    # Create .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating frontend .env file...")
        with open(env_file, 'w') as f:
            f.write("REACT_APP_API_URL=http://localhost:8000/api\n")
    
    os.chdir("..")
    return True

def create_sample_data():
    """Create sample data"""
    print("\n📊 Creating sample data...")
    
    # Determine python executable path
    venv_path = Path("healthcare_env")
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    success, _ = run_command([str(python_exe), "manage.py", "create_sample_data"])
    if success:
        print("✅ Sample data created successfully")
    else:
        print("⚠️  Failed to create sample data - you may need to configure database first")

def create_superuser():
    """Create Django superuser"""
    print("\n👤 Creating superuser...")
    
    # Determine python executable path
    venv_path = Path("healthcare_env")
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    # Run createsuperuser interactively
    subprocess.run([str(python_exe), "manage.py", "createsuperuser"])

def main():
    """Main setup function"""
    print("🏥 Healthcare Management System Setup")
    print("=====================================")
    
    if not check_requirements():
        sys.exit(1)
    
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Ask user preferences
    while True:
        create_super = input("\n🔑 Do you want to create a superuser? (y/n): ").lower().strip()
        if create_super in ['y', 'yes']:
            create_superuser()
            break
        elif create_super in ['n', 'no']:
            break
        else:
            print("Please enter 'y' or 'n'")
    
    while True:
        create_sample = input("\n📊 Do you want to create sample data? (y/n): ").lower().strip()
        if create_sample in ['y', 'yes']:
            create_sample_data()
            break
        elif create_sample in ['n', 'no']:
            break
        else:
            print("Please enter 'y' or 'n'")
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("1. Backend: python start_servers.py backend")
    print("2. Frontend: python start_servers.py frontend")
    print("3. Both: python start_servers.py")
    print("\nDefault URLs:")
    print("- Backend: http://localhost:8000")
    print("- Frontend: http://localhost:3000")
    print("- Admin: http://localhost:8000/admin")
    print("\nSample users (if created):")
    print("- Admin: admin@healthcare.com / admin123")
    print("- Doctor: dr.smith@healthcare.com / doctor123")
    print("- Patient: patient1@healthcare.com / patient123")

if __name__ == "__main__":
    main()