from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from .models import Patient
from .serializers import (
    PatientSerializer, PatientCreateSerializer, 
    PatientListSerializer, PatientUpdateSerializer
)
from accounts.permissions import IsAdminUser, IsPatientOrAdmin, IsOwnerOrReadOnly

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'blood_group']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['created_at', 'user__first_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Check if user already has a patient profile
        if hasattr(request.user, 'patient_profile'):
            return Response(
                {'error': 'Patient profile already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Only allow patients to create patient profiles
        if request.user.role != 'patient':
            return Response(
                {'error': 'Only users with patient role can create patient profiles'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    permission_classes = [IsPatientOrAdmin, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PatientUpdateSerializer
        return PatientSerializer


class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.patient_profile
        except Patient.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'error': 'Patient profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PatientStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_patients = Patient.objects.count()
        by_gender = Patient.objects.values('gender').annotate(
            count=models.Count('gender')
        )
        by_blood_group = Patient.objects.values('blood_group').annotate(
            count=models.Count('blood_group')
        )
        
        stats = {
            'total_patients': total_patients,
            'by_gender': list(by_gender),
            'by_blood_group': list(by_blood_group),
        }
        return Response(stats)
