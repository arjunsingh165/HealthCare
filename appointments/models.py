from django.db import models
from django.utils import timezone
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    APPOINTMENT_TYPE_CHOICES = (
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('checkup', 'Regular Checkup'),
        ('emergency', 'Emergency'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(blank=True)
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True, help_text="Doctor's notes after appointment")
    prescription = models.TextField(blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-created_at']
        unique_together = ('patient', 'doctor', 'appointment_date')

    def __str__(self):
        return f"{self.patient.user.full_name} -> Dr. {self.doctor.user.full_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_upcoming(self):
        return self.appointment_date > timezone.now()


class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.user.full_name} -> Dr. {self.doctor.user.full_name} ({self.rating}/5)"
    
    class Meta:
        unique_together = ('patient', 'doctor', 'appointment')
