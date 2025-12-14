"""
Serializers for the movies application.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Genre, Actor, Review


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""
    class Meta:
        model = Genre
        fields = ['id', 'name', 'created_at']


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for Actor model."""
    class Meta:
        model = Actor
        fields = ['id', 'name', 'bio', 'birth_date', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_id', 'movie', 'rating', 'text', 'created_at', 'updated_at']
        read_only_fields = ['user', 'user_id', 'created_at', 'updated_at']


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model."""
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), source='genres', write_only=True, required=False
    )
    actors = ActorSerializer(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), source='actors', write_only=True, required=False
    )
    average_rating = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_year', 'poster',
            'genres', 'genre_ids', 'actors', 'actor_ids',
            'average_rating', 'reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['is_staff']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user




