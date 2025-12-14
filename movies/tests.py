"""
Tests for the movies application.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Genre, Actor, Review


class MovieModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.actor = Actor.objects.create(name='Test Actor')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_year=2020
        )
        self.movie.genres.add(self.genre)
        self.movie.actors.add(self.actor)

    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Test Movie')

    def test_movie_average_rating(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Review.objects.create(user=user, movie=self.movie, rating=8, text='Great!')
        Review.objects.create(user=User.objects.create_user(username='user2', password='pass'), 
                             movie=self.movie, rating=6, text='Good')
        self.assertEqual(self.movie.average_rating, 7.0)




