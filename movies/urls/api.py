"""
API URL configuration for movies app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import MovieViewSet, GenreViewSet, ActorViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]




