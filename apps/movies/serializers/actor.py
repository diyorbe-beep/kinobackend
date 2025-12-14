"""
Serializer for Actor model.
"""
from rest_framework import serializers
from apps.movies.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for Actor model."""
    class Meta:
        model = Actor
        fields = ['id', 'uuid', 'name', 'slug', 'bio', 'birth_date', 'created_at']
        read_only_fields = ['id', 'uuid', 'slug', 'created_at']




