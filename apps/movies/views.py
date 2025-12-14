"""
Views for the movies application.
"""
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User

from .models import Movie, Genre, Actor, Review
from .serializers import (
    GenreSerializer,
    ActorSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewSerializer
)
from apps.shared.utils.custom_response import CustomResponse


class GenreListView(generics.ListAPIView):
    """List all genres."""
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Genre.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class ActorListView(generics.ListAPIView):
    """List all actors."""
    serializer_class = ActorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Actor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class MovieListView(generics.ListAPIView):
    """List all movies with filtering, search, and pagination."""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genres', 'release_year']
    search_fields = ['title', 'description', 'actors__name']
    ordering_fields = ['title', 'release_year', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related('genres', 'actors')
        
        # Filter by rating range
        min_rating = self.request.query_params.get('min_rating', None)
        max_rating = self.request.query_params.get('max_rating', None)
        
        if min_rating or max_rating:
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating'))
            if min_rating:
                queryset = queryset.filter(avg_rating__gte=float(min_rating))
            if max_rating:
                queryset = queryset.filter(avg_rating__lte=float(max_rating))
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class MovieDetailView(generics.RetrieveAPIView):
    """Get movie details by slug or id."""
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.all().prefetch_related('genres', 'actors', 'reviews')

    def get_object(self):
        """Get movie by slug or id."""
        lookup_value = self.kwargs.get('slug') or self.kwargs.get('pk')
        
        if not lookup_value:
            from rest_framework.exceptions import NotFound
            raise NotFound("Movie identifier not provided")
        
        # Try to get by slug first
        try:
            return self.get_queryset().get(slug=lookup_value)
        except Movie.DoesNotExist:
            # If not found by slug, try by id
            try:
                return self.get_queryset().get(id=int(lookup_value))
            except (ValueError, Movie.DoesNotExist):
                # If still not found, raise 404
                from rest_framework.exceptions import NotFound
                raise NotFound("Movie not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class MovieCreateView(generics.CreateAPIView):
    """Create a new movie (admin only)."""
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                request=request,
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.validation_error(
            errors=serializer.errors,
            request=request
        )


class MovieUpdateView(generics.UpdateAPIView):
    """Update a movie (admin only)."""
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Movie.objects.all()

    def get_object(self):
        """Get movie by slug or id."""
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field or 'slug')
        
        # Try to get by slug first
        try:
            return self.get_queryset().get(slug=lookup_value)
        except Movie.DoesNotExist:
            # If not found by slug, try by id
            try:
                return self.get_queryset().get(id=int(lookup_value))
            except (ValueError, Movie.DoesNotExist):
                # If still not found, raise 404
                from rest_framework.exceptions import NotFound
                raise NotFound("Movie not found")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                request=request,
                data=serializer.data
            )
        return CustomResponse.validation_error(
            errors=serializer.errors,
            request=request
        )


class MovieDeleteView(generics.DestroyAPIView):
    """Delete a movie (admin only)."""
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Movie.objects.all()

    def get_object(self):
        """Get movie by slug or id."""
        lookup_value = self.kwargs.get('slug') or self.kwargs.get('pk')
        
        if not lookup_value:
            from rest_framework.exceptions import NotFound
            raise NotFound("Movie identifier not provided")
        
        # Try to get by slug first
        try:
            return self.get_queryset().get(slug=lookup_value)
        except Movie.DoesNotExist:
            # If not found by slug, try by id
            try:
                return self.get_queryset().get(id=int(lookup_value))
            except (ValueError, Movie.DoesNotExist):
                # If still not found, raise 404
                from rest_framework.exceptions import NotFound
                raise NotFound("Movie not found")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            status_code=status.HTTP_204_NO_CONTENT
        )


class SearchMoviesView(generics.ListAPIView):
    """Search movies by query."""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query:
            return Movie.objects.none()
        
        return Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(actors__name__icontains=query)
        ).distinct().prefetch_related('genres')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={
                'query': request.query_params.get('q', ''),
                'results': serializer.data,
                'count': len(serializer.data)
            }
        )


class ReviewListView(generics.ListAPIView):
    """List reviews for a movie."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie', None)
        queryset = Review.objects.all().select_related('user', 'movie')
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class ReviewCreateView(generics.CreateAPIView):
    """Create a review."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                request=request,
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.validation_error(
            errors=serializer.errors,
            request=request
        )




