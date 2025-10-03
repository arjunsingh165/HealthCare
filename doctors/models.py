from django.db import models
from accounts.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('general_medicine', 'General Medicine'),
        ('gynecology', 'Gynecology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('pulmonology', 'Pulmonology'),
        ('urology', 'Urology'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    hospital_affiliation = models.CharField(max_length=200, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True, help_text="Comma-separated languages")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.get_specialization_display()}"
    
    class Meta:
        ordering = ['-rating', 'user__first_name']
