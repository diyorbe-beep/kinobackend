"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls.v1')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Health check endpoint
@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({'status': 'ok', 'service': 'Movie API'})

urlpatterns += [
    path('health/', health_check, name='health-check'),
]




