from rest_framework import serializers
from .models import Doctor
from accounts.serializers import UserProfileSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('user', 'rating', 'total_reviews')
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class DoctorListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ('id', 'user_name', 'user_email', 'specialization', 'specialization_display', 
                 'years_of_experience', 'consultation_fee', 'rating', 'is_available')


class DoctorPublicSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ('id', 'user_name', 'profile_picture', 'specialization', 'specialization_display',
                 'years_of_experience', 'bio', 'consultation_fee', 'available_from', 'available_to',
                 'is_available', 'hospital_affiliation', 'languages_spoken', 'rating', 'total_reviews')


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('user', 'rating', 'total_reviews', 'created_at')
