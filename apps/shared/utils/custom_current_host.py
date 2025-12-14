"""
Utility functions for getting client information from request.
"""
from typing import Optional
from django.http import HttpRequest


def get_current_host(request: HttpRequest) -> Optional[str]:
    """Get current host from request."""
    if not request:
        return None
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{scheme}://{host}"


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """Get client IP address from request."""
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')




