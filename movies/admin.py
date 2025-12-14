"""
Admin configuration for movies app.
"""
from django.contrib import admin
from .models import Movie, Genre, Actor, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'created_at']
    search_fields = ['name']
    list_filter = ['birth_date']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['release_year', 'genres', 'created_at']
    filter_horizontal = ['genres', 'actors']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    search_fields = ['user__username', 'movie__title', 'text']
    list_filter = ['rating', 'created_at']




