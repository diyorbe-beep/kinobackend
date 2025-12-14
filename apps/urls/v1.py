"""
Main URL configuration for API v1.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from apps.shared.utils.custom_response import CustomResponse


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    
    if not all([username, email, password, password_confirm]):
        return CustomResponse.validation_error(
            errors={'detail': 'All fields are required'},
            request=request
        )
    
    if password != password_confirm:
        return CustomResponse.validation_error(
            errors={'password': "Passwords don't match"},
            request=request
        )
    
    if User.objects.filter(username=username).exists():
        return CustomResponse.validation_error(
            errors={'username': 'Username already exists'},
            request=request
        )
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    
    return CustomResponse.success(
        message_key="SUCCESS_MESSAGE",
        request=request,
        data={
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        status_code=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def profile(request):
    """Get current user profile."""
    return CustomResponse.success(
        message_key="SUCCESS_MESSAGE",
        request=request,
        data={
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': request.user.is_staff,
        }
    )


urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/profile/', profile, name='profile'),
    path('movies/', include('apps.movies.urls.v1')),
]




