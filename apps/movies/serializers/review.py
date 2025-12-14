"""
Serializer for Review model.
"""
from rest_framework import serializers
from apps.movies.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'uuid', 'user', 'user_id', 'movie', 'rating', 'text',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uuid', 'user', 'user_id', 'created_at', 'updated_at']




