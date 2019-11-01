from django.db import models
from django.conf import settings

class Genre(models.Model):
   name = models.CharField(max_length=50)

class Movie(models.Model):
   title = models.CharField(max_length=200)
   audience = models.IntegerField()
   poster_url = models.CharField(max_length=500)
   description = models.TextField()
   genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')

class Review(models.Model):
   content = models.CharField(max_length=100)
   score = models.IntegerField()
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews_movie')
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_user')
