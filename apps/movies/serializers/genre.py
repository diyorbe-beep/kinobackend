"""
Serializer for Genre model.
"""
from rest_framework import serializers
from apps.movies.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""
    class Meta:
        model = Genre
        fields = ['id', 'uuid', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'uuid', 'slug', 'created_at']




