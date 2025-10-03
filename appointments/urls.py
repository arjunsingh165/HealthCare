from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/status/', views.UpdateAppointmentStatusView.as_view(), name='appointment-status'),
    path('doctor/', views.DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('patient/', views.PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('stats/', views.AppointmentStatsView.as_view(), name='appointment-stats'),
    
    # Reviews
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('doctors/<int:doctor_id>/reviews/', views.DoctorReviewsView.as_view(), name='doctor-reviews'),
]