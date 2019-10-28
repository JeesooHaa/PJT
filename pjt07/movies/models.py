from django.db import models
from django.conf import settings


class Movie(models.Model):

    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    audience = models.IntegerField()
    open_date = models.DateField(max_length=20)
    genre = models.CharField(max_length=50)
    watch_grade = models.CharField(max_length=10)
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')


class Comment(models.Model):

    content = models.CharField(max_length=50)
    score = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
