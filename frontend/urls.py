from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.doctors_list, name='doctors'),
    path('appointments/', views.appointments, name='appointments'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('approve-appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject-appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('complete-appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path('patients/', views.patients, name='patients'),
    path('chat/', views.chat, name='chat'),
    path('chat/messages/<int:appointment_id>/', views.get_chat_messages, name='get_chat_messages'),
    path('profile/', views.profile, name='profile'),
]