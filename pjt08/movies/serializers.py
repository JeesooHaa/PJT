from rest_framework import serializers
from .models import Genre, Movie, Review

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', )


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'audience', 'poster_url', 'description', 'genre' )


class GenreListSerializer(GenreSerializer):
    # related name
    movies = MovieSerializer(many=True)

    class Meta:
        model = Genre
        fields = ('id', 'movies', 'name', )


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        # movie_id, user_id 로 해야됨
        fields = ('id', 'content', 'score', 'movie_id', 'user_id', )
