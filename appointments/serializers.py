from rest_framework import serializers
from .models import Appointment, Review
from patients.serializers import PatientListSerializer
from doctors.serializers import DoctorListSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer(read_only=True)
    doctor = DoctorListSerializer(read_only=True)
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('doctor', 'appointment_date', 'appointment_type', 'reason_for_visit', 'symptoms')
    
    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'patient_profile'):
            validated_data['patient'] = user.patient_profile
        else:
            raise serializers.ValidationError("Only patients can create appointments")
        return super().create(validated_data)


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status', 'notes', 'prescription', 'follow_up_date', 'rejection_reason')


class AppointmentListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ('id', 'patient_name', 'doctor_name', 'doctor_specialization', 
                 'appointment_date', 'appointment_type', 'status', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('patient', 'doctor', 'appointment')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('appointment', 'rating', 'comment')
    
    def create(self, validated_data):
        appointment = validated_data['appointment']
        user = self.context['request'].user
        
        if not hasattr(user, 'patient_profile'):
            raise serializers.ValidationError("Only patients can create reviews")
        
        if appointment.patient != user.patient_profile:
            raise serializers.ValidationError("You can only review your own appointments")
        
        if appointment.status != 'completed':
            raise serializers.ValidationError("You can only review completed appointments")
        
        validated_data['patient'] = user.patient_profile
        validated_data['doctor'] = appointment.doctor
        
        return super().create(validated_data)
