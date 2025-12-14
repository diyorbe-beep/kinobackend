"""
Serializers for Movie model.
"""
from rest_framework import serializers
from apps.movies.models import Movie
from .genre import GenreSerializer
from .actor import ActorSerializer


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view."""
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'uuid', 'title', 'slug', 'poster', 'release_year',
            'genres', 'average_rating', 'created_at'
        ]
        read_only_fields = ['id', 'uuid', 'slug', 'created_at']

    def get_average_rating(self, obj):
        """Get average rating."""
        return obj.average_rating


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view."""
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'uuid', 'title', 'slug', 'description', 'release_year',
            'poster', 'genres', 'actors', 'average_rating', 'reviews_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uuid', 'slug', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        """Get average rating."""
        return obj.average_rating

    def get_reviews_count(self, obj):
        """Get reviews count."""
        return obj.reviews.count()




