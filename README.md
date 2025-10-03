# Healthcare Management System Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis (for channels)

## Quick Setup

### Option 1: Python Setup Script (Recommended - Cross-platform)
```bash
python setup.py
```

### Option 2: PowerShell Setup Script (Windows)
```powershell
# Basic setup
.\setup.ps1

# With superuser and sample data
.\setup.ps1 -CreateSuperuser -CreateSampleData

# Backend only (skip frontend)
.\setup.ps1 -SkipFrontend
```

### Option 3: Manual Setup
```bash
python -m venv healthcare_env
# Windows
healthcare_env\Scripts\activate
# Linux/Mac
source healthcare_env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
POSTGRES_DB=healthcare_db
POSTGRES_USER=healthcare_user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
ACCESS_TOKEN_LIFETIME_HOURS=24
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb healthcare_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Load Sample Data (Optional)
```bash
python manage.py loaddata fixtures/sample_data.json
```

## Starting the Application

### Option 1: Python Server Manager (Recommended)
```bash
# Start both servers
python start_servers.py

# Start only backend
python start_servers.py backend

# Start only frontend  
python start_servers.py frontend
```

### Option 2: PowerShell Server Manager (Windows)
```powershell
# Start both servers
.\start_servers.ps1

# Start only backend
.\start_servers.ps1 backend

# Start only frontend
.\start_servers.ps1 frontend
```

### Option 3: Manual Start
```bash
# Backend
healthcare_env\Scripts\activate  # Windows
# source healthcare_env/bin/activate  # Linux/Mac
python manage.py runserver

# Frontend (in new terminal)
cd frontend
npm start
```

## Manual Setup (if not using scripts)

### 1. Create Virtual Environment
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Variables
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### 4. Start Development Server
```bash
npm start
```

## Production Deployment

### Backend (Django)
1. Set DEBUG=False in .env
2. Configure allowed hosts
3. Set up static file serving
4. Configure database for production
5. Set up SSL certificates

### Frontend (React)
1. Build the application: `npm run build`
2. Serve static files using nginx or similar
3. Configure proper routing

## Features Implemented

### ✅ Admin Features
- CRUD operations for all users and appointments
- Comprehensive admin dashboard
- User statistics and analytics
- Role-based access control

### ✅ Patient Features
- User registration and profile management
- Doctor search and filtering
- Appointment booking system
- Real-time chat with doctors
- Appointment history and status tracking

### ✅ Doctor Features
- Professional profile management
- Patient list and appointment management
- Accept/reject appointment requests
- Real-time chat with patients
- Prescription and notes management

### ✅ General User Features
- Read-only access to doctor listings
- Doctor profiles and ratings
- Specialization browsing

### ✅ Technical Features
- JWT authentication with refresh tokens
- PostgreSQL database backend
- Django Channels for real-time chat
- RESTful API with filtering and pagination
- Responsive React frontend
- Modern UI with Tailwind CSS

## API Endpoints

### Authentication
- POST `/api/accounts/register/` - User registration
- POST `/api/accounts/login/` - User login
- POST `/api/accounts/token/refresh/` - Refresh token
- GET/PATCH `/api/accounts/profile/` - User profile

### Patients
- GET/POST `/api/patients/` - List/Create patients
- GET/PATCH/DELETE `/api/patients/{id}/` - Patient details
- GET `/api/patients/profile/` - Current user's patient profile

### Doctors
- GET/POST `/api/doctors/` - List/Create doctors
- GET/PATCH/DELETE `/api/doctors/{id}/` - Doctor details
- GET `/api/doctors/available/` - Available doctors
- GET `/api/doctors/specialization/{spec}/` - Doctors by specialization

### Appointments
- GET/POST `/api/appointments/` - List/Create appointments
- GET/PATCH/DELETE `/api/appointments/{id}/` - Appointment details
- POST `/api/appointments/{id}/accept/` - Accept appointment
- POST `/api/appointments/{id}/reject/` - Reject appointment
- POST `/api/appointments/{id}/complete/` - Complete appointment

### Chat
- GET/POST `/api/chat/rooms/` - Chat rooms
- GET `/api/chat/rooms/{id}/` - Chat room details
- GET/POST `/api/chat/rooms/{id}/messages/` - Messages
- POST `/api/chat/rooms/{id}/mark-read/` - Mark messages as read

## Default Users
After running migrations and creating superuser, you can create test users:

### Admin User
- Email: @healthcare.com
- Password: 
- Role: admin

### Doctor User
- Email: @healthcare.com
- Password: 
- Role: doctor

### Patient User
- Email: healthcare.com
- Password:
- Role: patient

## Troubleshooting

### Common Issues
1. **Database connection errors**: Check PostgreSQL is running and credentials are correct
2. **JWT token errors**: Ensure secret key is set and tokens haven't expired
3. **Chat not working**: Verify Redis is running for Django Channels
4. **CORS errors**: Check API URL configuration in frontend

### Development Tips
1. Use Django admin panel for quick data management
2. Enable debug mode for detailed error messages
3. Check browser console for frontend errors
4. Use API documentation at `/admin/doc/` if enabled

## License
This project is licensed under the MIT License.#

