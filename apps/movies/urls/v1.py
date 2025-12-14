"""
URL configuration for movies app v1.
"""
from django.urls import path
from .. import views

app_name = 'movies'

urlpatterns = [
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('actors/', views.ActorListView.as_view(), name='actor-list'),
    path('', views.MovieListView.as_view(), name='movie-list'),
    path('search/', views.SearchMoviesView.as_view(), name='movie-search'),
    path('create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),
    # Movie detail, update, delete - supports both slug and id
    path('<str:slug>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('<str:slug>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('<str:slug>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
]




