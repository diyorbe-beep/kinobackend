"""
Views for the movies application.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q, Avg
try:
    from django_filters.rest_framework import DjangoFilterBackend
except ImportError:
    DjangoFilterBackend = None
from .models import Movie, Genre, Actor, Review
from .serializers import (
    MovieSerializer, GenreSerializer, ActorSerializer,
    ReviewSerializer, UserSerializer
)
import csv
from django.http import HttpResponse
from io import StringIO


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Movie model with search, filter, and sorting.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    if DjangoFilterBackend:
        filter_backends.insert(0, DjangoFilterBackend)
    search_fields = ['title', 'description', 'actors__name']
    ordering_fields = ['title', 'release_year', 'created_at', 'average_rating']
    ordering = ['-created_at']

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        """Enhanced queryset with filtering and rating range."""
        queryset = super().get_queryset()
        
        # Filter by genre
        genre_id = self.request.query_params.get('genres', None)
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id).distinct()
        
        # Filter by release year
        year = self.request.query_params.get('release_year', None)
        if year:
            queryset = queryset.filter(release_year=year)
        
        # Filter by rating range (average rating)
        min_rating = self.request.query_params.get('min_rating', None)
        max_rating = self.request.query_params.get('max_rating', None)
        
        if min_rating or max_rating:
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating'))
            if min_rating:
                queryset = queryset.filter(avg_rating__gte=float(min_rating))
            if max_rating:
                queryset = queryset.filter(avg_rating__lte=float(max_rating))
        
        return queryset

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific movie."""
        movie = self.get_object()
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def import_csv(self, request):
        """Import movies from CSV file."""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(decoded_file))
        
        imported = 0
        errors = []
        
        for row in csv_reader:
            try:
                # Create or get genres
                genre_names = [g.strip() for g in row.get('genres', '').split(',') if g.strip()]
                genres = []
                for genre_name in genre_names:
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    genres.append(genre)
                
                # Create or get actors
                actor_names = [a.strip() for a in row.get('actors', '').split(',') if a.strip()]
                actors = []
                for actor_name in actor_names:
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    actors.append(actor)
                
                # Create movie
                movie = Movie.objects.create(
                    title=row.get('title', ''),
                    description=row.get('description', ''),
                    release_year=int(row.get('release_year', 0)),
                )
                movie.genres.set(genres)
                movie.actors.set(actors)
                imported += 1
            except Exception as e:
                errors.append(f"Row {row.get('title', 'unknown')}: {str(e)}")
        
        return Response({
            'imported': imported,
            'errors': errors
        })


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Genre model (read-only for non-admins)."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Actor model (read-only for non-admins)."""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter reviews by movie if movie_id is provided."""
        queryset = super().get_queryset()
        movie_id = self.request.query_params.get('movie', None)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review."""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Set permissions - users can only edit their own reviews."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Users can only see all reviews, but only edit their own."""
        queryset = super().get_queryset()
        if self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(user=self.request.user)
        return queryset

