"""
Admin configuration for movies app.
"""
from django.contrib import admin
from .models import Movie, Genre, Actor, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'birth_date', 'created_at']
    search_fields = ['name']
    list_filter = ['birth_date']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'release_year', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['release_year', 'genres', 'created_at']
    filter_horizontal = ['genres', 'actors']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    search_fields = ['user__username', 'movie__title', 'text']
    list_filter = ['rating', 'created_at']




