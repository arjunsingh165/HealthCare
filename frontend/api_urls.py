from django.urls import path, include

# API URL patterns - consolidating all API routes
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('chat/', include('chat.urls')),
]