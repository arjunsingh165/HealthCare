from rest_framework import serializers
from .models import Patient
from accounts.serializers import UserProfileSerializer

class PatientSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    bmi = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = '__all__'


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('user',)
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class PatientListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Patient
        fields = ('id', 'user_name', 'user_email', 'gender', 'blood_group', 'created_at')


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('user', 'created_at')
