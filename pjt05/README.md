# Project 05

## 목차

1. [데이터베이스](https://github.com/JeesooHaa/PJT/blob/master/pjt05#1-데이터베이스)
2. [영화 목록 페이지](https://github.com/JeesooHaa/PJT/blob/master/pjt05#2-영화-목록-페이지)
3. [영화 정보 생성](https://github.com/JeesooHaa/PJT/blob/master/pjt05#3-영화-정보-생성)
4. [영화 정보 조회](https://github.com/JeesooHaa/PJT/blob/master/pjt05#4-영화-정보-조회)
5. [영화 정보 수정](https://github.com/JeesooHaa/PJT/blob/master/pjt05#5-영화-정보-수정)
6. [영화 정보 삭제](https://github.com/JeesooHaa/PJT/blob/master/pjt05#6-영화-정보-삭제)



### 1. 데이터베이스

##### movies app 의 model.py 에 작성 후 `migrate`

```python
# model.py

from django.db import models

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
```



### 2. 영화 목록 페이지

##### `/movies/` 접근,  `title`, `score`, 링크 설정

```python
# views.py

from .models import Movie


def movies(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/movies.html', context)
```

```html
<!-- movies.html -->

{% extends 'base.html' %}

{% block title %}영화 목록{% endblock %}

{% block content %}
<a href="/movies/new/">새 영화 등록</a>

<ul>
  {% for movie in movies %}
  <li><a href="/movies/{{ movie.pk }}/">{{ movie.title }}</a> {{ movie.score }}</li>
  {% endfor %}
</ul>

{% endblock %}
```




### 3. 영화 정보 생성

##### new.html 에서 영화 정보를 받아 view.py 의 `create` 함수에서 DB 에 저장 

```python
# views.py

def new(request):
    return render(request, 'movies/new.html')


# response한 정보들을 DB에 저장
def create(request):
    title = request.GET.get('title')
    title_en = request.GET.get('title_en')
    audience = request.GET.get('audience')
    open_date = request.GET.get('open_date')
    genre = request.GET.get('genre')
    watch_grade = request.GET.get('watch_grade')
    score = request.GET.get('score')
    poster_url = request.GET.get('poster_url')
    description = request.GET.get('description')
    movie = Movie(title=title, title_en=title_en, audience=audience, open_date=open_date, genre=genre, watch_grade=watch_grade, score=score, poster_url=poster_url, description=description)
    movie.save()
    return render(request, 'movies/create.html')
```

```html
<!--new.html-->
<!--영화 정보를 입력받는 form 작성-->

{% extends 'base.html' %}

{% block title %}영화 정보 생성 Form{% endblock %}

{% block content %}
<h1>영화 정보 작성</h1>
<form action="/movies/create/">
  <label for="title">TITLE</label><br>
  <input id="title" type="text" name="title"><br>
  <label for="title_en">TITLE_EN</label><br>
  <input id="title_en" type="text" name="title_en"><br>
  <label for="audience">audience</label><br>
  <input id="audience" type="number" name="audience"><br>  
  <label for="open_date">open_date</label><br>
  <input id="open_date" type="date" name="open_date"><br>
  <label for="genre">genre</label><br>
  <input id="genre" type="text" name="genre"><br>
  <label for="watch_grade">watch_grade</label><br>
  <input id="watch_grade" type="text" name="watch_grade"><br>
  <label for="score">score</label><br>
  <input id="score" type="number" name="score"><br>
  <label for="poster_url">poster_url</label><br>
  <input id="poster_url" type="text" name="poster_url"><br>
  <label for="description">description</label><br>
  <textarea id="description" name="description"></textarea><br>
  <button type="submit">작성하기</button>
</form>
{% endblock %}
```



### 4. 영화 정보 조회

##### primary key 를 사용해 영화 정보에 접근하는 페이지 작성 

```python
# urls.py

urlpatterns = [
	...
    path('<int:movie_pk>/edit/', views.edit),
    ...
]
```

```python
# view.py

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)
```

```html
<!--detail.html-->

{% extends 'base.html' %}

{% block title %}{{ movie.title }}{% endblock %}

{% block content %}
  <h1>{{ movie.title }}</h1>
  <p>{{ movie.title_en }}</p>
  <p>{{ movie.audience }}</p>
  <p>{{ movie.open_date }}</p>
  <p>{{ movie.watch_grade }}</p>
  <p>{{ movie.genre }}</p>
  <p>{{ movie.score }}</p>
  <p>{{ movie.poster_url }}</p>
  <p>{{ movie.description }}</p>

  <!--목록, 수정, 삭제 링크-->
  <a href="/movies/">목록</a>
  <a href="/movies/{{ movie.pk }}/edit/">수정</a>
  <a href="/movies/{{ movie.pk }}/delete/">삭제</a>
{% endblock %}
```



### 5. 영화 정보 수정

##### DB 의 영화 정보를 불러와 수정 후 다시 저장 

```python
# views.py

def edit(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    # open_date = movie.open_date
    context = {
        'movie': movie,
        # 'open_date': open_date,
    }
    return render(request, 'movies/edit.html', context)


# 수정된 데이터 저장 
def update(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.title = request.GET.get('title')
    movie.title_en = request.GET.get('title_en')
    movie.audience = request.GET.get('audience')
    movie.open_date = request.GET.get('open_date')
    movie.genre = request.GET.get('genre')
    movie.watch_grade = request.GET.get('watch_grade')
    movie.score = request.GET.get('score')
    movie.poster_url = request.GET.get('poster_url')
    movie.description = request.GET.get('description')
    movie.save()
    context = {
        'movie': movie,
    }
    return render(request, 'movies/update.html', context)
```

```html
<!--edit.html-->
<!--영화 정보를 수정하는 form 작성-->

{% extends 'base.html' %}

{% block title %}영화 정보 수정 Form{% endblock %}

<!--date, textarea 주의!!-->
{% block content %}
<h1>영화 정보 수정</h1>
<form action="/movies/{{ movie.pk }}/update/">
  <label for="title">TITLE</label><br>
  <input id="title" type="text" name="title" value="{{ movie.title }}"><br>
  <label for="title_en">TITLE_EN</label><br>
  <input id="title_en" type="text" name="title_en" value="{{ movie.title_en }}"><br>
  <label for="audience">audience</label><br>
  <input id="audience" type="number" name="audience" value="{{ movie.audience }}"><br>  
  <label for="open_date">open_date</label><br>
  <input id="open_date" type="date" name="open_date" value="{{ movie.open_date|date:"Y-m-d" }}"><br>
  {% comment %} <h1>{{ open_date|date:"Y-m-d" }}</h1> {% endcomment %}
  <label for="genre">genre</label><br>
  <input id="genre" type="text" name="genre" value="{{ movie.genre }}"><br>
  <label for="watch_grade">watch_grade</label><br>
  <input id="watch_grade" type="text" name="watch_grade" value="{{ movie.watch_grade }}"><br>
  <label for="score">score</label><br>
  <input id="score" type="number" name="score" value="{{ movie.score }}"><br>
  <label for="poster_url">poster_url</label><br>
  <input id="poster_url" type="text" name="poster_url" value="{{ movie.poster_url }}"><br>
  <label for="description">description</label><br>
  <textarea id="description" name="description">{{ movie.description }}</textarea><br>
  <button type="submit">수정하기</button>
</form>
{% endblock %}
```



### 6. 영화 정보 삭제

##### primary key 로 접근해서 삭제!

```python
# model.py

def delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return render(request, 'movies/delete.html')
```

```html
<!--delete.html-->

{% extends 'base.html' %}

{% block title %}영화 정보 삭제{% endblock %}

{% block content %}
<h1 class="text-center">영화 정보 삭제가 완료되었습니다.</h1>
<p class="text-center"><a href="/movies/">영화 정보 목록</a></p>
{% endblock %}
```

