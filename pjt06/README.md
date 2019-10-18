# Project 06

## 목차

1. [데이터베이스](https://github.com/JeesooHaa/PJT/blob/master/pjt06#1-데이터베이스)
2. [영화 목록 페이지](https://github.com/JeesooHaa/PJT/blob/master/pjt06#2-영화-목록-페이지)
3. [영화 정보 생성](https://github.com/JeesooHaa/PJT/blob/master/pjt06#3-영화-정보-생성)
4. [영화 정보 조회](https://github.com/JeesooHaa/PJT/blob/master/pjt06#4-영화-정보-조회)
5. [영화 정보 수정](https://github.com/JeesooHaa/PJT/blob/master/pjt06#5-영화-정보-수정)
6. [영화 정보 삭제](https://github.com/JeesooHaa/PJT/blob/master/pjt06#6-영화-정보-삭제)
7. [영화 한줄평 생성](https://github.com/JeesooHaa/PJT/blob/master/pjt06#7-영화-한줄평-생성)



#### # Project 05 와 중복되는 내용은 생략합니다.

### 1. 데이터베이스

##### - 한줄평 테이블 생성 

```python
# model.py

from django.db import models

...

class Comment(models.Model):

    content = models.CharField(max_length=50)
    score = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
```



### 2. 영화 목록 페이지

##### - `static` 을 사용해 이미지 삽입 

```html
<!-- movies.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}Movies{% endblock %}

{% block content %}

<img src="{% static '/movies/images/movie.jpg/' %}" alt="movie"><hr>

<a href="{% url 'movies:create' %}">새 영화 등록</a>

<ul>
  {% for movie in movies %}
  <li><a href="{% url 'movies:detail' movie.pk %}">{{ movie.title }}</a> {{ movie.score }}</li>
  {% endfor %}
</ul>

{% endblock %}
```




### 3. 영화 정보 생성

##### - forms.py 에서 영화 정보를 받을 수 있는 `form` 작성

##### - views.py 에서 `POST` 요청이 왔을 때만 영화 정보를 입력할 수 있도록 함 

```python
# forms.py

from django import forms
from .models import Movie, Comment

YEARS= [x for x in range(1940,2021)]


class MovieForm(forms.ModelForm):

    open_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
    )

    class Meta:
        model = Movie
        fields = '__all__'
```

```python
# views.py

def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else: 
        form = MovieForm()
    context = {'form': form}
    return render(request, 'movies/create.html', context)
```

```html
<!--create.html-->

{% extends 'base.html' %}

{% block title %}Movie::Create{% endblock title %}

{% block content %}
<form method="POST">
  {% csrf_token %}
  {{form.as_p}}
  <button type="submit">Create</button>
</form>
{% endblock %}
```



### 4. 영화 정보 조회

##### - `@require_GET` 을 사용해  `GET` 요청이 왔을 때만 `detail` 함수가 실행되게 함
```python
# view.py

@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comments = movie.comments.all()
    form = CommentForm()
    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
    }
    return render(request, 'movies/detail.html', context)
```



### 5. 영화 정보 수정

##### DB 의 영화 정보를 불러와 수정 후 다시 저장 

```python
# views.py

def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = MovieForm(instance=movie)
    context = {'form':form}
    return render(request, 'movies/update.html', context)
```

```html
<!--update.html-->

{% extends 'base.html' %}

{% block title %}Movie::Update{% endblock title %}

{% block content %}
<form method="POST">
  {% csrf_token %}
  {{form.as_p}}
  <button type="submit">Update</button>
</form>
{% endblock content %}
```



### 6. 영화 정보 삭제

##### - `@require_POST` 을 사용해  `POST` 요청이 왔을 때만 `delete` 함수가 실행되게 함

```python
# views.py

@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect('movies:movies')
```



### 7. 영화 한줄평 생성 

##### - forms.py 에서 `	CommentForm` 생성 
##### - views.py 에서 `	movie_pk` 를 `comment` 에 저장 후 DB에 입력
```python
# forms.py

class CommentForm(forms.ModelForm):

    content = forms.CharField(
        label='한줄평',
    )

    class Meta:
        model = Comment
        fields = ['content', 'score', ]
```

```python
# views.py

@require_POST
def reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie_id = movie_pk
        comment.save()
        return redirect('movies:detail', movie_pk)
```

```django
<!--detail.html-->

  {% for comment in comments %}
    <p>{{ comment.pk }}. {{ comment.content }} {{ comment.score }}</p>
  {% endfor %}

  <form action="{% url 'movies:reviews' movie.pk %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Comment Create</button>
  </form>
```

