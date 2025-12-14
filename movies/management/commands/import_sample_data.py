"""
Management command to import sample movie data.
"""
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Actor, Review
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


class Command(BaseCommand):
    help = 'Imports sample movie data'

    def handle(self, *args, **options):
        # Create genres
        genres_data = [
            'Action', 'Adventure', 'Comedy', 'Drama', 'Horror',
            'Sci-Fi', 'Thriller', 'Romance', 'Fantasy', 'Crime'
        ]
        genres = {}
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres[genre_name] = genre
            if created:
                self.stdout.write(f'Created genre: {genre_name}')

        # Create actors
        actors_data = [
            {'name': 'Tom Hanks', 'birth_date': date(1956, 7, 9)},
            {'name': 'Leonardo DiCaprio', 'birth_date': date(1974, 11, 11)},
            {'name': 'Meryl Streep', 'birth_date': date(1949, 6, 22)},
            {'name': 'Robert De Niro', 'birth_date': date(1943, 8, 17)},
            {'name': 'Scarlett Johansson', 'birth_date': date(1984, 11, 22)},
        ]
        actors = {}
        for actor_data in actors_data:
            actor, created = Actor.objects.get_or_create(
                name=actor_data['name'],
                defaults={'birth_date': actor_data['birth_date']}
            )
            actors[actor_data['name']] = actor
            if created:
                self.stdout.write(f'Created actor: {actor_data["name"]}')

        # Create movies
        movies_data = [
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'release_year': 1994,
                'genres': ['Drama', 'Crime'],
                'actors': ['Tom Hanks', 'Robert De Niro']
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_year': 2008,
                'genres': ['Action', 'Crime', 'Drama'],
                'actors': ['Leonardo DiCaprio']
            },
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_year': 2010,
                'genres': ['Action', 'Sci-Fi', 'Thriller'],
                'actors': ['Leonardo DiCaprio', 'Tom Hanks']
            },
            {
                'title': 'Pulp Fiction',
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'release_year': 1994,
                'genres': ['Crime', 'Drama'],
                'actors': ['Robert De Niro', 'Meryl Streep']
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'release_year': 1999,
                'genres': ['Action', 'Sci-Fi'],
                'actors': ['Scarlett Johansson']
            },
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['description'],
                    'release_year': movie_data['release_year'],
                }
            )
            if created:
                # Set genres
                movie_genres = [genres[g] for g in movie_data['genres'] if g in genres]
                movie.genres.set(movie_genres)
                # Set actors
                movie_actors = [actors[a] for a in movie_data['actors'] if a in actors]
                movie.actors.set(movie_actors)
                self.stdout.write(f'Created movie: {movie_data["title"]}')

        # Create sample reviews if users exist
        user = User.objects.first()
        if user:
            for movie in Movie.objects.all()[:3]:
                Review.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={
                        'rating': 9,
                        'text': f'Great movie! Highly recommended. {movie.title} is a masterpiece.'
                    }
                )
            self.stdout.write('Created sample reviews')

        self.stdout.write(self.style.SUCCESS('Sample data import completed!'))




