"""
Custom CORS middleware for flexible origin handling.
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re


class FlexibleCorsMiddleware(MiddlewareMixin):
    """
    Development rejimida barcha localhost va local network originlarini ruxsat beradi.
    Production rejimida faqat belgilangan originlar ruxsat etiladi.
    """
    
    def process_request(self, request):
        """Request ni qayta ishlash."""
        # CORS preflight request ni qayta ishlash
        if request.method == 'OPTIONS':
            origin = request.META.get('HTTP_ORIGIN', '')
            if self._is_allowed_origin(origin):
                return None
        return None
    
    def process_response(self, request, response):
        """Response ga CORS headerlarini qo'shish."""
        origin = request.META.get('HTTP_ORIGIN', '')
        
        if self._is_allowed_origin(origin):
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = (
                'Content-Type, Authorization, X-CSRFToken, X-Requested-With, Accept'
            )
            response['Access-Control-Max-Age'] = '86400'
        
        return response
    
    def _is_allowed_origin(self, origin):
        """Origin ruxsat etilganligini tekshirish."""
        if not origin:
            return False
        
        # Production rejimida faqat belgilangan originlar
        if not settings.DEBUG:
            allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            return origin in allowed_origins
        
        # Development rejimida localhost va local network
        localhost_patterns = [
            r'^http://localhost:\d+$',
            r'^http://127\.0\.0\.1:\d+$',
            r'^http://192\.168\.\d+\.\d+:\d+$',
            r'^http://10\.\d+\.\d+\.\d+:\d+$',
        ]
        
        for pattern in localhost_patterns:
            if re.match(pattern, origin):
                return True
        
        # Belgilangan originlar ham ruxsat etiladi
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        return origin in allowed_origins

