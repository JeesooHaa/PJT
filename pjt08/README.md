# Project 08

## 목차

1. [데이터베이스](https://github.com/JeesooHaa/PJT/blob/master/pjt08#1-데이터베이스)
2. [Serializers](https://github.com/JeesooHaa/PJT/blob/master/pjt08#2-Serializers)
3. [영화 정보, 장르 정보 GET](https://github.com/JeesooHaa/PJT/blob/master/pjt08#3-영화-정보-장르-정보-GET)
4. [리뷰 생성 ](https://github.com/JeesooHaa/PJT/blob/master/pjt08#4-리뷰-생성)
5. [리뷰 정보 조회, 수정, 삭제](https://github.com/JeesooHaa/PJT/blob/master/pjt08#5-리뷰-정보-조회-수정-삭제)
6. [API documents](https://github.com/JeesooHaa/PJT/blob/master/pjt08#6-API-documents)




### 1. 데이터베이스

##### - 모델 생성 

```python
# models.py

from django.db import models
from django.conf import settings

class Genre(models.Model):
   name = models.CharField(max_length=50)

class Movie(models.Model):
   title = models.CharField(max_length=200)
   audience = models.IntegerField()
   poster_url = models.CharField(max_length=500)
   description = models.TextField()
   # related_name 을 하지 않으면 serilalizer 만들때 문제가 생길 수 있음
   genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')

class Review(models.Model):
   content = models.CharField(max_length=100)
   score = models.IntegerField()
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews_movie')
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_user')
```



### 2. Serializers

##### - 요청을 JSON 형식의 파일로 바꾸기 위해 serializer 생성

```python
# serializers.py

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
        # movie_id, user_id 로 하지 않으면 view 에서 id 를 받을 때 인식하지 못한다.
        fields = ('id', 'content', 'score', 'movie_id', 'user_id', )
```



### 3. 영화 정보, 장르 정보 GET

##### - 영화 정보 또는 장르 정보를 GET method 요청이 왔을 때 보여줌

```python
# views.py

@api_view(['GET'])
def genres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


# 해당 장르를 genre_id 로 가지는 영화의 목록을 보여주기 위해 GenreListSerializer 사용
@api_view(['GET'])
def genres_list(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreListSerializer(genre)
    return Response(serializer.data)


@api_view(['GET'])
def movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
```



### 4. 리뷰 생성 

##### - POST 요청이 왔을 때 리뷰를 작성 

##### - id 를 받을 때 serializer field 에 정의된 이름과 같은 곳에 받아야함 

```python
# view.py

@api_view(['POST'])
def movie_review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk, user_id=1)
    return Response({"message": "작성되었습니다."})
```



### 5. 리뷰 정보 조회, 수정, 삭제

##### -  같은 URL 에서 method 의 종류에 따라 다른 기능을 수행

##### - GET : 정보 조회 / PUT : 수정 / DELETE : 삭제 

```python
# views.py

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delte(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "수정되었습니다."})
    else: 
        review.delete()
        return Response({"message": "삭제되었습니다."})
```



### 6. API documents

```python
# urls.py

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Movie API',
        default_version='v1',
        description='영화 관련 API 서비스입니다.',
    )
)

app_name = 'movies'
urlpatterns = [
	...

    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
]
```

![swagger](https://github.com/JeesooHaa/PJT/blob/master/pjt08/img/swagger.PNG)
