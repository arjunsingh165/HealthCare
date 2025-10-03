from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('stats/', views.UserStatsView.as_view(), name='user-stats'),
    
    # Legacy endpoints for backward compatibility
    path('register-legacy/', views.RegisterView.as_view(), name='register-legacy'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
]