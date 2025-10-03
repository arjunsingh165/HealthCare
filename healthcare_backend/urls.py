from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('frontend.api_urls')),  # API routes
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),  # Redirect Django auth to frontend
    path('accounts/logout/', RedirectView.as_view(url='/login/', permanent=True)),  # Redirect logout
    path('', include('frontend.urls')),  # Frontend routes
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)