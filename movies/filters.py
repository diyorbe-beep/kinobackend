"""
Custom filters for movies app (optional, for advanced filtering).
"""
from django_filters import rest_framework as filters
from .models import Movie


class MovieFilter(filters.FilterSet):
    """Custom filter set for Movie model."""
    release_year = filters.NumberFilter(field_name='release_year')
    genres = filters.NumberFilter(field_name='genres', lookup_expr='exact')
    
    class Meta:
        model = Movie
        fields = ['genres', 'release_year']




