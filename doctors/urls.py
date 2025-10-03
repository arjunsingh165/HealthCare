from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('available/', views.AvailableDoctorsView.as_view(), name='available-doctors'),
    path('specialization/<str:specialization>/', views.DoctorsBySpecializationView.as_view(), name='doctors-by-specialization'),
    path('stats/', views.DoctorStatsView.as_view(), name='doctor-stats'),
]