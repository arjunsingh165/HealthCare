from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('profile/', views.PatientProfileView.as_view(), name='patient-profile'),
    path('stats/', views.PatientStatsView.as_view(), name='patient-stats'),
]