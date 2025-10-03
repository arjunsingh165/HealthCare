from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from .models import Doctor
from .serializers import (
    DoctorSerializer, DoctorCreateSerializer, 
    DoctorListSerializer, DoctorPublicSerializer, DoctorUpdateSerializer
)
from accounts.permissions import IsAdminUser, IsDoctorOrAdmin, IsOwnerOrReadOnly

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialization', 'hospital_affiliation']
    ordering_fields = ['created_at', 'user__first_name', 'rating', 'years_of_experience']
    ordering = ['-rating', 'user__first_name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DoctorCreateSerializer
        return DoctorListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]  # Public list for general users
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Check if user already has a doctor profile
        if hasattr(request.user, 'doctor_profile'):
            return Response(
                {'error': 'Doctor profile already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Only allow doctors to create doctor profiles
        if request.user.role != 'doctor':
            return Response(
                {'error': 'Only users with doctor role can create doctor profiles'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    permission_classes = [permissions.AllowAny]  # Public view for general users
    
    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and (user.role in ['doctor', 'admin'] and 
                                     (user.role == 'admin' or self.get_object().user == user)):
            if self.request.method in ['PUT', 'PATCH']:
                return DoctorUpdateSerializer
            return DoctorSerializer
        return DoctorPublicSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsDoctorOrAdmin, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.doctor_profile
        except Doctor.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'error': 'Doctor profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DoctorsBySpecializationView(generics.ListAPIView):
    serializer_class = DoctorPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'years_of_experience', 'consultation_fee']
    ordering = ['-rating']
    
    def get_queryset(self):
        specialization = self.kwargs.get('specialization')
        return Doctor.objects.filter(
            specialization=specialization, 
            is_available=True
        )


class DoctorStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_doctors = Doctor.objects.count()
        available_doctors = Doctor.objects.filter(is_available=True).count()
        by_specialization = Doctor.objects.values('specialization').annotate(
            count=models.Count('specialization')
        )
        avg_rating = Doctor.objects.aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating']
        
        stats = {
            'total_doctors': total_doctors,
            'available_doctors': available_doctors,
            'by_specialization': list(by_specialization),
            'average_rating': round(avg_rating, 2) if avg_rating else 0,
        }
        return Response(stats)


class AvailableDoctorsView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    ordering_fields = ['rating', 'years_of_experience', 'consultation_fee']
    ordering = ['-rating']
