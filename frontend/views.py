from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import User
import requests
from django.conf import settings
import json
from datetime import datetime, date, time
from django.utils import timezone

def home(request):
    """Home page with overview of the healthcare system"""
    context = {
        'title': 'Healthcare Management System',
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'frontend/home.html', context)

def login_view(request):
    """Login page and handling"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            # Redirect to dashboard or next URL
            next_url = request.GET.get('next', 'frontend:dashboard')
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'frontend/login.html')

def logout_view(request):
    """Logout and redirect to home"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('frontend:home')

def register_view(request):
    """Registration page and handling"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number', '')
        date_of_birth = request.POST.get('date_of_birth') or None
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        elif role not in ['patient', 'doctor', 'user']:
            messages.error(request, 'Invalid role selected.')
        else:
            try:
                # Create user
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth
                )
                
                messages.success(request, f'Registration successful! You can now login as a {role}.')
                return redirect('frontend:login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'frontend/register.html')

@login_required
def dashboard(request):
    """Enhanced dashboard with real-time messaging"""
    user = request.user
    context = {
        'user': user,
        'role': user.role,
        'title': f'{user.role.title()} Dashboard'
    }
    
    from appointments.models import Appointment
    from doctors.models import Doctor
    from patients.models import Patient
    from chat.models import ChatRoom, Message
    
    # Add role-specific data with messaging
    if user.role == 'patient':
        try:
            patient = Patient.objects.get(user=user)
            
            # Get patient's accepted appointments for messaging
            accepted_appointments = Appointment.objects.filter(
                patient=patient,
                status='accepted'
            ).select_related('doctor__user').order_by('-appointment_date')
            
            # Get recent appointments
            recent_appointments = Appointment.objects.filter(
                patient=patient
            ).select_related('doctor__user').order_by('-created_at')[:5]
            
            # Get recent messages from doctors
            recent_messages = Message.objects.filter(
                chat_room__patient=user,
                sender__role='doctor'
            ).select_related('sender', 'chat_room__appointment__doctor__user').order_by('-timestamp')[:5]
            
            context.update({
                'template': 'frontend/patient_dashboard.html',
                'patient': patient,
                'accepted_appointments': accepted_appointments,
                'recent_appointments': recent_appointments,
                'recent_messages': recent_messages,
                'total_appointments': Appointment.objects.filter(patient=patient).count(),
                'pending_appointments': Appointment.objects.filter(patient=patient, status='pending').count(),
                'accepted_count': accepted_appointments.count(),
            })
            
        except Patient.DoesNotExist:
            context['template'] = 'frontend/patient_dashboard.html'
            
    elif user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=user)
            
            # Get doctor's accepted appointments for messaging
            accepted_appointments = Appointment.objects.filter(
                doctor=doctor,
                status='accepted'
            ).select_related('patient__user').order_by('-appointment_date')
            
            # Get pending appointments for review
            pending_appointments = Appointment.objects.filter(
                doctor=doctor,
                status='pending'
            ).select_related('patient__user').order_by('-created_at')
            
            # Get recent appointments
            recent_appointments = Appointment.objects.filter(
                doctor=doctor
            ).select_related('patient__user').order_by('-created_at')[:5]
            
            # Get recent messages from patients
            recent_messages = Message.objects.filter(
                chat_room__doctor=user,
                sender__role='patient'
            ).select_related('sender', 'chat_room__appointment__patient__user').order_by('-timestamp')[:5]
            
            context.update({
                'template': 'frontend/doctor_dashboard.html',
                'doctor': doctor,
                'accepted_appointments': accepted_appointments,
                'pending_appointments': pending_appointments,
                'recent_appointments': recent_appointments,
                'recent_messages': recent_messages,
                'total_appointments': Appointment.objects.filter(doctor=doctor).count(),
                'pending_count': pending_appointments.count(),
                'accepted_count': accepted_appointments.count(),
            })
            
        except Doctor.DoesNotExist:
            context.update({
                'template': 'frontend/doctor_dashboard.html',
                'error': 'Please complete your doctor profile first.'
            })
    elif user.role == 'admin':
        context['template'] = 'frontend/admin_dashboard.html'
    else:
        context['template'] = 'frontend/user_dashboard.html'
    
    return render(request, 'frontend/dashboard.html', context)

def doctors_list(request):
    """Public doctors listing - only registered doctors"""
    from doctors.models import Doctor
    
    doctors = Doctor.objects.select_related('user').filter(user__is_active=True)
    
    # Get unique specializations for the filter
    specializations = Doctor.objects.filter(
        specialization__isnull=False
    ).exclude(specialization='').values_list('specialization', flat=True).distinct()
    
    context = {
        'title': 'Our Doctors',
        'doctors': doctors,
        'specializations': specializations,
    }
    return render(request, 'frontend/doctors.html', context)

@login_required
def appointments(request):
    """Improved appointments page with clear view of all appointments"""
    user = request.user
    context = {'user': user, 'title': 'Appointments'}
    
    from appointments.models import Appointment
    from doctors.models import Doctor
    from patients.models import Patient
    
    if user.role == 'patient':
        # Get patient's appointments
        try:
            patient = Patient.objects.get(user=user)
            appointments = Appointment.objects.filter(
                patient=patient
            ).select_related('doctor__user').order_by('-appointment_date')
        except Patient.DoesNotExist:
            appointments = Appointment.objects.none()
        
        # Get available doctors for new bookings
        doctors = Doctor.objects.select_related('user').filter(user__is_active=True)
        
        context.update({
            'appointments': appointments,
            'doctors': doctors,
            'title': 'My Appointments',
            'can_book': True
        })
        
    elif user.role == 'doctor':
        # Get doctor's appointments
        try:
            doctor = Doctor.objects.get(user=user)
            appointments = Appointment.objects.filter(
                doctor=doctor
            ).select_related('patient__user').order_by('-appointment_date')
            
            context.update({
                'appointments': appointments,
                'doctor': doctor,
                'title': 'Patient Appointments',
                'can_manage': True
            })
        except Doctor.DoesNotExist:
            messages.error(request, 'Please complete your doctor profile first.')
            return redirect('frontend:profile')
            
    elif user.role == 'admin':
        # Admin sees all appointments
        appointments = Appointment.objects.all().select_related(
            'patient__user', 'doctor__user'
        ).order_by('-appointment_date')
        
        context.update({
            'appointments': appointments,
            'title': 'All Appointments',
            'is_admin': True
        })
    
    return render(request, 'frontend/appointments.html', context)

@login_required
def patients(request):
    """Patients page with role-based access"""
    user = request.user
    
    if user.role == 'doctor':
        # Doctors see appointment requests and their patients
        from appointments.models import Appointment
        from patients.models import Patient
        
        # Get appointments for this doctor
        try:
            from doctors.models import Doctor
            doctor = Doctor.objects.get(user=user)
            
            # Get all patients with appointments to this doctor
            patients = Patient.objects.filter(
                appointments__doctor=doctor
            ).select_related('user').distinct()
            
            # Add pending appointment info to each patient
            for patient in patients:
                pending_appointment = Appointment.objects.filter(
                    patient=patient, 
                    doctor=doctor, 
                    status='pending'
                ).first()
                patient.pending_appointment = pending_appointment
                
                # Set current doctor for confirmed appointments
                confirmed_appointment = Appointment.objects.filter(
                    patient=patient, 
                    doctor=doctor, 
                    status='confirmed'
                ).first()
                if confirmed_appointment:
                    patient.current_doctor = doctor
            
            context = {
                'title': 'My Patients',
                'user': user,
                'patients': patients,
                'doctor': doctor
            }
        except Doctor.DoesNotExist:
            messages.error(request, 'Please complete your doctor profile first.')
            return redirect('frontend:profile')
            
    elif user.role == 'admin':
        # Admin sees all patients
        from patients.models import Patient
        patients = Patient.objects.select_related('user').all()
        
        context = {
            'title': 'All Patients',
            'user': user,
            'patients': patients
        }
    else:
        # General users see patient-doctor mappings (confirmed appointments)
        from appointments.models import Appointment
        from patients.models import Patient
        
        # Get patients with confirmed appointments
        confirmed_appointments = Appointment.objects.filter(
            status='confirmed'
        ).select_related('patient__user', 'doctor__user')
        
        patients = []
        for appointment in confirmed_appointments:
            patient = appointment.patient
            patient.current_doctor = appointment.doctor
            patients.append(patient)
        
        context = {
            'title': 'Patient-Doctor Mappings',
            'user': user,
            'patients': patients
        }
    
    return render(request, 'frontend/patients.html', context)

@login_required
@login_required
@login_required
def chat(request):
    """Chat page with real functionality"""
    user = request.user
    chat_partner_id = request.GET.get('partner')
    appointment_id = request.GET.get('appointment')
    
    from doctors.models import Doctor
    from patients.models import Patient
    from appointments.models import Appointment
    from chat.models import ChatRoom, Message
    
    context = {
        'title': 'Messages',
        'user': request.user
    }
    
    # Handle POST request for sending messages
    if request.method == 'POST':
        message_content = request.POST.get('message', '').strip()
        appointment_id = request.POST.get('appointment_id')
        
        if message_content and appointment_id:
            try:
                appointment = Appointment.objects.get(
                    id=appointment_id,
                    status='accepted'
                )
                
                # Verify user has access to this chat
                if (user.role == 'doctor' and appointment.doctor.user == user) or \
                   (user.role == 'patient' and appointment.patient.user == user):
                    
                    # Get or create chat room
                    chat_room, created = ChatRoom.objects.get_or_create(
                        appointment=appointment,
                        defaults={
                            'patient': appointment.patient.user,
                            'doctor': appointment.doctor.user,
                            'is_active': True
                        }
                    )
                    
                    # Create message
                    Message.objects.create(
                        chat_room=chat_room,
                        sender=user,
                        content=message_content,
                        message_type='text'
                    )
                    
                    # Return JSON response for AJAX requests
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({
                            'success': True,
                            'message': 'Message sent successfully'
                        })
                    else:
                        # Redirect back to the same chat
                        return redirect(f"{request.path}?partner={chat_partner_id}&appointment={appointment_id}")
                        
            except Appointment.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid appointment'
                    })
    
    # Get chat conversations based on user role
    if user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=user)
            # Get all accepted appointments for this doctor
            accepted_appointments = Appointment.objects.filter(
                doctor=doctor,
                status='accepted'
            ).select_related('patient__user')
            
            # Create conversations list
            conversations = []
            for apt in accepted_appointments:
                # Get or create chat room for message count
                chat_room, created = ChatRoom.objects.get_or_create(
                    appointment=apt,
                    defaults={
                        'patient': apt.patient.user,
                        'doctor': apt.doctor.user,
                        'is_active': True
                    }
                )
                
                # Get latest message
                latest_message = Message.objects.filter(chat_room=chat_room).order_by('-timestamp').first()
                
                conversations.append({
                    'partner': apt.patient.user,
                    'appointment': apt,
                    'partner_name': apt.patient.user.get_full_name(),
                    'partner_role': 'Patient',
                    'latest_message': latest_message.content[:30] + '...' if latest_message else 'No messages yet',
                    'latest_time': latest_message.timestamp if latest_message else apt.created_at,
                    'unread_count': Message.objects.filter(
                        chat_room=chat_room,
                        sender=apt.patient.user,
                        is_read=False
                    ).count()
                })
            
            context['conversations'] = conversations
            
        except Doctor.DoesNotExist:
            context['error'] = 'Please complete your doctor profile first.'
            
    elif user.role == 'patient':
        try:
            patient = Patient.objects.get(user=user)
            # Get all accepted appointments for this patient
            accepted_appointments = Appointment.objects.filter(
                patient=patient,
                status='accepted'
            ).select_related('doctor__user')
            
            # Create conversations list
            conversations = []
            for apt in accepted_appointments:
                # Get or create chat room for message count
                chat_room, created = ChatRoom.objects.get_or_create(
                    appointment=apt,
                    defaults={
                        'patient': apt.patient.user,
                        'doctor': apt.doctor.user,
                        'is_active': True
                    }
                )
                
                # Get latest message
                latest_message = Message.objects.filter(chat_room=chat_room).order_by('-timestamp').first()
                
                conversations.append({
                    'partner': apt.doctor.user,
                    'appointment': apt,
                    'partner_name': f'Dr. {apt.doctor.user.get_full_name()}',
                    'partner_role': 'Doctor',
                    'latest_message': latest_message.content[:30] + '...' if latest_message else 'No messages yet',
                    'latest_time': latest_message.timestamp if latest_message else apt.created_at,
                    'unread_count': Message.objects.filter(
                        chat_room=chat_room,
                        sender=apt.doctor.user,
                        is_read=False
                    ).count()
                })
            
            context['conversations'] = conversations
            
        except Patient.DoesNotExist:
            context['error'] = 'Please complete your patient profile first.'
    
    # If specific chat partner is selected, get chat messages
    if chat_partner_id and appointment_id:
        try:
            appointment = Appointment.objects.get(
                id=appointment_id,
                status='accepted'
            )
            
            # Verify user has access to this chat
            if (user.role == 'doctor' and appointment.doctor.user == user) or \
               (user.role == 'patient' and appointment.patient.user == user):
                
                # Get or create chat room
                chat_room, created = ChatRoom.objects.get_or_create(
                    appointment=appointment,
                    defaults={
                        'patient': appointment.patient.user,
                        'doctor': appointment.doctor.user,
                        'is_active': True
                    }
                )
                
                # Get all messages in this chat room
                messages = Message.objects.filter(
                    chat_room=chat_room
                ).select_related('sender').order_by('timestamp')
                
                # Mark messages as read for the current user
                Message.objects.filter(
                    chat_room=chat_room,
                    is_read=False
                ).exclude(sender=user).update(is_read=True)
                
                context['active_chat'] = {
                    'appointment': appointment,
                    'partner': User.objects.get(id=chat_partner_id),
                    'messages': messages,
                    'chat_room': chat_room
                }
                
        except (Appointment.DoesNotExist, User.DoesNotExist):
            context['error'] = 'Chat conversation not found.'
    
    return render(request, 'frontend/chat.html', context)

@login_required
def get_chat_messages(request, appointment_id):
    """AJAX endpoint to get chat messages"""
    from django.http import JsonResponse
    from chat.models import ChatRoom, Message
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(
            id=appointment_id,
            status='accepted'
        )
        
        # Verify user has access to this chat
        user = request.user
        if not ((user.role == 'doctor' and appointment.doctor.user == user) or \
                (user.role == 'patient' and appointment.patient.user == user)):
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        # Get chat room
        chat_room = ChatRoom.objects.filter(appointment=appointment).first()
        if not chat_room:
            return JsonResponse({'messages': []})
        
        # Get messages
        messages = Message.objects.filter(
            chat_room=chat_room
        ).select_related('sender').order_by('timestamp')
        
        # Mark unread messages as read
        Message.objects.filter(
            chat_room=chat_room,
            is_read=False
        ).exclude(sender=user).update(is_read=True)
        
        # Format messages for JSON response
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'content': msg.content,
                'sender_name': msg.sender.get_full_name(),
                'is_own_message': msg.sender == user,
                'timestamp': msg.timestamp.strftime('%M d, %H:%i'),
                'timestamp_iso': msg.timestamp.isoformat()
            })
        
        return JsonResponse({
            'messages': messages_data,
            'success': True
        })
        
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def profile(request):
    """User profile page with role-specific functionality"""
    user = request.user
    
    if request.method == 'POST':
        # Update user profile
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.date_of_birth = request.POST.get('date_of_birth') or user.date_of_birth
        user.address = request.POST.get('address', user.address)
        user.save()
        
        # Handle patient-specific profile creation
        if user.role == 'patient':
            from patients.models import Patient
            patient, created = Patient.objects.get_or_create(user=user)
            
            # Update patient-specific fields
            patient.symptoms = request.POST.get('symptoms', patient.symptoms)
            patient.medical_history = request.POST.get('medical_history', patient.medical_history)
            patient.allergies = request.POST.get('allergies', patient.allergies)
            patient.emergency_contact_name = request.POST.get('emergency_contact_name', patient.emergency_contact_name)
            patient.emergency_contact_phone = request.POST.get('emergency_contact_phone', patient.emergency_contact_phone)
            patient.save()
            
            messages.success(request, 'Patient profile updated successfully!')
        
        # Handle doctor-specific profile creation  
        elif user.role == 'doctor':
            from doctors.models import Doctor
            doctor, created = Doctor.objects.get_or_create(user=user)
            
            # Update doctor-specific fields
            doctor.specialization = request.POST.get('specialization', doctor.specialization)
            doctor.license_number = request.POST.get('license_number', doctor.license_number)
            doctor.experience_years = request.POST.get('experience_years', doctor.experience_years)
            doctor.education = request.POST.get('education', doctor.education)
            doctor.consultation_fee = request.POST.get('consultation_fee', doctor.consultation_fee)
            doctor.save()
            
            messages.success(request, 'Doctor profile updated successfully!')
        else:
            messages.success(request, 'Profile updated successfully!')
        
        return redirect('frontend:profile')
    
    # Get role-specific profile data
    context = {
        'title': 'My Profile',
        'user': user
    }
    
    if user.role == 'patient':
        from patients.models import Patient
        try:
            context['patient'] = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            context['patient'] = None
    elif user.role == 'doctor':
        from doctors.models import Doctor
        try:
            context['doctor'] = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            context['doctor'] = None
    
    return render(request, 'frontend/profile.html', context)


@login_required
def book_appointment(request):
    """Book appointment view for patients"""
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('frontend:dashboard')
    
    from doctors.models import Doctor
    from patients.models import Patient
    from appointments.models import Appointment
    from datetime import datetime, date
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms')
        medical_history = request.POST.get('medical_history')
        allergies = request.POST.get('allergies')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_phone = request.POST.get('emergency_contact_phone')
        additional_notes = request.POST.get('additional_notes')
        appointment_type = request.POST.get('appointment_type', 'consultation')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            
            # Get or create patient profile
            patient, created = Patient.objects.get_or_create(user=request.user)
            
            # Update patient information
            patient.symptoms = symptoms
            patient.medical_history = medical_history
            patient.allergies = allergies
            patient.emergency_contact_name = emergency_contact_name
            patient.emergency_contact_phone = emergency_contact_phone
            patient.save()
            
            # Update user profile
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            if request.POST.get('date_of_birth'):
                user.date_of_birth = request.POST.get('date_of_birth')
            user.save()
            
            # Create appointment with combined date and time
            appointment_datetime = datetime.combine(
                datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                datetime.strptime(appointment_time, '%H:%M').time()
            )
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=timezone.make_aware(appointment_datetime),
                reason_for_visit=symptoms,
                symptoms=symptoms,
                appointment_type=appointment_type,
                status='pending'
            )
            
            messages.success(request, f'Appointment request sent to Dr. {doctor.user.get_full_name()}. You will be notified once approved.')
            return redirect('frontend:appointments')
            
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor not found.')
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
    
    # GET request - show booking form
    context = {
        'doctors': Doctor.objects.filter(user__is_active=True),
        'selected_doctor': request.GET.get('doctor'),
        'tomorrow': date.today().replace(day=date.today().day + 1),
    }
    
    # Get patient data if exists
    try:
        context['patient'] = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        context['patient'] = None
    
    return render(request, 'frontend/book_appointment.html', context)


@login_required
def approve_appointment(request, appointment_id):
    """Approve appointment request"""
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can approve appointments.')
        return redirect('frontend:dashboard')
    
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
        appointment.status = 'accepted'
        appointment.save()
        
        messages.success(request, f'Appointment with {appointment.patient.user.get_full_name()} has been approved.')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return redirect('frontend:patients')


@login_required
def reject_appointment(request, appointment_id):
    """Reject appointment request"""
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can reject appointments.')
        return redirect('frontend:dashboard')
    
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
        appointment.status = 'rejected'
        appointment.save()
        
        messages.info(request, f'Appointment with {appointment.patient.user.get_full_name()} has been rejected.')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return redirect('frontend:patients')


@login_required
def complete_appointment(request, appointment_id):
    """Mark appointment as completed"""
    if request.user.role != 'doctor':
        messages.error(request, 'Only doctors can mark appointments as completed.')
        return redirect('frontend:dashboard')
    
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
        appointment.status = 'completed'
        appointment.save()
        
        messages.success(request, f'Appointment with {appointment.patient.user.get_full_name()} marked as completed.')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return redirect('frontend:appointments')