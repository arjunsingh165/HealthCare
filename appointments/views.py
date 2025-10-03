from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from django.utils import timezone
from .models import Appointment, Review
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer, 
    AppointmentListSerializer, AppointmentUpdateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)
from accounts.permissions import (
    IsAdminUser, IsPatient, IsDoctor, IsDoctorOrAdmin, 
    IsAppointmentParticipant, IsPatientOrAdmin
)

class AppointmentListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type', 'doctor__specialization']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['-appointment_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        elif user.role == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        else:
            return Appointment.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsPatient]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    permission_classes = [IsAppointmentParticipant]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer
    
    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        user = request.user
        
        # Only doctors can update appointment status
        if 'status' in request.data and user.role != 'doctor':
            return Response(
                {'error': 'Only doctors can update appointment status'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only the assigned doctor can update the appointment
        if user.role == 'doctor' and appointment.doctor.user != user:
            return Response(
                {'error': 'You can only update your own appointments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsDoctor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['appointment_date']
    
    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)


class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['-appointment_date']
    
    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)


class AppointmentStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_appointments = Appointment.objects.count()
        by_status = Appointment.objects.values('status').annotate(
            count=models.Count('status')
        )
        by_type = Appointment.objects.values('appointment_type').annotate(
            count=models.Count('appointment_type')
        )
        today_appointments = Appointment.objects.filter(
            appointment_date__date=timezone.now().date()
        ).count()
        
        stats = {
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'by_status': list(by_status),
            'by_type': list(by_type),
        }
        return Response(stats)


# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'doctor__specialization']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Review.objects.all()
        elif user.role == 'patient':
            return Review.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            return Review.objects.filter(doctor__user=user)
        else:
            return Review.objects.all()  # Public reviews for general users
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsPatient]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class DoctorReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return Review.objects.filter(doctor_id=doctor_id)


class UpdateAppointmentStatusView(APIView):
    permission_classes = [IsDoctor]
    
    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, doctor__user=request.user)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Appointment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected', 'completed']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = new_status
        if new_status == 'rejected':
            appointment.rejection_reason = request.data.get('rejection_reason', '')
        appointment.save()
        
        return Response(AppointmentSerializer(appointment).data)
