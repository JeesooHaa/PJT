# PJT 10

### 0. 프로젝트 목표

- django DB 모델링

- accounts, movies 기능 구현

- Git을 통한 협업

  

---

### 1. django setting



#### 1.1. 잊지말자 가상환경!

- vs code에서 python 이 3.7 버전인지 확인하자

```bash
$ python -V
```

- venv 로 3.7 버전 잡고, `python -m venv venv` 
- `ctrl + shift + p`로 venv 환경 잡기
- kill terminal 후, 다시 terminal 켜서 가상환경 잡히는 지 확인!



#### 1.2. pip install

- `pip list` 쳐서 pip 설치 목록 확인 후 pip 업그레이드

- django 설치

  ```bash
  $ pip install django
  ```

- **★여기서 협업을 위한 작업이 필요함★**

  - 팀원이 모듈 하나하나 `pip install` 해야하는 번거로움을 줄여주기 위해 `pip freeze` 를 활용하자

    ```bash 
    $ pip freeze > requirements.txt
    ```

  - 팀원은 `pip install -r requirements.txt`만 해주면 알아서 requirements에 깔린 모듈들을 다 설치하게 됨

    

### 1.3. gitignore

- `touch .gitignore`해서 gitignore할 파일 생성 후,

- gitignore.io 가서 venv, windows, visualstudio code, django, python 으로 gitignore 파일 생성 후, 프로젝트 내 gitignore 파일에 복붙하기 

  - 맨 왼쪽 소스제어 새로고침해서 gitignore 적용 되는 지 확인

    

#### 그럼 준비 다 끝났으니 django 프로젝트를 시작해보자!



---

### 2. django 시작



#### 2.1. django 프로젝트 생성

- `pjt10`이름으로 프로젝트 만들기

  ```bash
  $ django-admin startproject pjt10 .
  ```

  - 잊지말자 뒤에 `.`!!!!!!

- 서버 잘 켜지는 지 확인하기(a.k.a 로켓)

  ```bash
  $ python manage.py runserver
  ```

- 프로젝트가 생성되었으니 settings.py 작업 하기

  - 그전에! vs code extensions에서 django가 깔렸는 지 확인하기

    - 안 깔려있으면 이 workspace에서만 enable로 설정하기

    - .vscode/settings.json으로 가서 django extensions에 있던 코드 긁어서 복붙하기

      ```json
      {
          "python.pythonPath": "venv\\Scripts\\python.exe",
          "files.associations": {
              "**/templates/*.html": "django-html",
              "**/templates/*": "django-txt",
              "**/requirements{/**,*}.{txt,in}": "pip-requirements"
          },
          "emmet.includeLanguages": {"django-html": "html"},
          "[django-html]": {
            "editor.tabSize": 2
          }
      }
      
      ```

      - tabSize는 추가 설정임

  - 다시 pjt10/settings.py로 가서

    - 언어, 시간 설정 수정

    ```python
    LANGUAGE_CODE = 'ko-kr'
    
    TIME_ZONE = 'Asia/Seoul'
    ```

- 겸사겸사 base.html도 만들자

  - pjt10/templates/base.html

    ```html
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <script src="https://kit.fontawesome.com/58a4b12f94.js" crossorigin="anonymous"></script>
      <title>{% block title %}{% endblock %}</title>
    </head>
    <body>
      {% block content %}{% endblock %}  
    </body>
    </html>
    
    ```

    - 만약! base.html 아이콘이 이상하다?! 면 django extensions가 disabled 된 것!

  - pjt10/settings.py에서 basedir 설정!

    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'pjt10', 'templates')],
            
    ```

    

#### 2.2. django 앱 생성(accounts, movies)



- 귀찮으니 한번에 앱 만들자

  ```bash
  $ python manage.py startapp accounts
  $ python manage.py startapp movies
  ```

  - 앱 이름은 보통 복수로 짓는다

- 앱 만들었으니 pjt10/settings.py에 출생신고 하러 가자

  ```python
  INSTALLED_APPS = [
      # local apps
      'movies',
      'accounts',
  
  ```



#### 모든 준비는 끝났다 ! 지금부턴 APP 작업 시작



---

### 3. DB 모델링



#### 3.1.  `User` 모델링

- 우리는 accounts에서 새로운 user 모델을 정의해서 쓸 것이다(== 유저모델 커스터마이징)

- accounts/models.py

  ```python
  from django.db import models
  from django.contrib.auth.models import AbstractUser
  from django.conf import settings
  
  class User(AbstractUser):
      # followers랑 user m:n
      followers = models.ManyToManyField(
          settings.AUTH_USER_MODEL,
          # 역.참.조
          related_name='followings',
      )
  
  ```

  - contrib, conf 헷갈리지 말자!

- pjt10/settings.py로 가서 cutomize한 user_model 사용하겠다는 내용 작성

  ```python
  AUTH_USER_MODEL = 'accounts.User'
  
  ```
  
  

#### 3.2. `movies` DB 모델링

- 명세를 보고 1:n, m:n 결정해서 모델링을 진행한다

- movies/models.py

  - Genre, Movie, Review 모델

  ```python
  from django.db import models
  from django.conf import settings
  
  
  class Genre(models.Model):
      name = models.CharField(max_length=20)
  
  
  class Movie(models.Model):
      title = models.CharField(max_length=30)
      audience = models.IntegerField()
      poster_url = models.CharField(max_length=140)
      description = models.TextField()
      # movie 와 genre 는 m:n
      genres = models.ManyToManyField(Genre, related_name='movies')
      liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')
  
  
  class Review(models.Model):
      content = models.CharField(max_length=140)
      score = models.IntegerField()
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
      
  ```



#### DB 모델링이 끝났으면 `migrate` 하러 가자!

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

- `migrate` 한 후, `ctrl+shift+p`해서 `sqlite3` 실행하기



#### 모델링도 끝났으니 본격적으로 app 기능 구현 시작!



---

### 4. accounts app 기능구현

- 구현해야 할 기능
  - 회원가입, 로그인, 로그아웃, 회원 상세정보 조회

- 그전에! pjt10/urls.py에서 accounts, movies를 include 해주는 작업 필요하다

  - appname 설정한것

  ```python
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('movies/', include('movies.urls')),
      path('accounts/', include('accounts.urls')),
  ]
  
  ```

  

#### 4.1. 회원가입 구현

- urls.py 파일 생성하기

  ```python
  # urls.py
  from django.urls import path
  from . import views
  
  app_name = 'accounts'
  urlpatterns = [
      path('signup/', views.signup, name='signup'),
  ]
  
  ```

- 우리는 cutom한 usercreation form을 사용할 것이므로 forms.py 만들자

  - accounts/forms.py

    ```python
    from django.contrib.auth.forms import UserChangeForm, UserCreationForm
    from django.contrib.auth import get_user_model
    
    class CustomUserCreationForm(UserCreationForm):
    
        class Meta:
            model = get_user_model()
            fields = UserCreationForm.Meta.fields
            
    ```

    

- views.py

  ```python
  from django.shortcuts import render, redirect, get_object_or_404
  from django.contrib.auth.forms import AuthenticationForm
  from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash 
  from django.contrib.auth.decorators import login_required
  from django.views.decorators.http import require_POST
  from .forms import CustomUserCreationForm
  from .models import User
  
  def signup(request):
      if request.user.is_authenticated:
          return redirect('movies:index')
      if request.method == 'POST':
          form = CustomUserCreationForm(request.POST)
          if form.is_valid():
              user = form.save()
              auth_login(request, user)
              return redirect('movies:index')
      else: # == 'GET'
          form = CustomUserCreationForm()
      context = {'form': form}
      return render(request, 'accounts/signup.html', context)
  
  ```

- templates/accounts/signup.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}가입하기{% endblock title %}
  
  {% block content %}
  <form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">SUBMIT</button>
  </form>
  {% endblock content %}
  
  ```

- 서버 켜서 accounts/signup/으로 접근했을 때, 회원가입창이 잘 뜨는 지 확인하기!



#### 4.2. 로그인 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'accounts'
  urlpatterns = [
      path('signup/', views.signup, name='signup'),
      path('login/', views.login, name='login'),
      
  ```

- views.py

  ```python
  def login(request):
      if request.user.is_authenticated:
          return redirect('movies:index')
      if request.method == 'POST':
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
              auth_login(request, form.get_user())
              next_page = request.GET.get('next')
              return redirect(next_page or 'movies:index')
      else:
          form = AuthenticationForm()
      context = {'form': form}
      return render(request, 'accounts/login.html', context)
  
  ```

- templates/accounts/login.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}로그인{% endblock title %}
  
  {% block content %}
  <form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">SUBMIT</button>
  </form>
  {% endblock content %}
  
  ```



#### 4.3.  로그아웃 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'accounts'
  urlpatterns = [
      path('signup/', views.signup, name='signup'),
      path('login/', views.login, name='login'),
      path('logout/', views.logout, name='logout'),
      
  ```

- views.py

```python
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

```



#### 4.4. 회원 목록/ 회원 상세정보 조회 기능 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'accounts'
  urlpatterns = [
      path('signup/', views.signup, name='signup'),
      path('login/', views.login, name='login'),
      path('logout/', views.logout, name='logout'),
      path('', views.index, name='index'),
      path('<int:user_pk>/', views.detail, name='detail'),
  ]
  
  ```

- views.py

  ```python
  def index(request):
      users = User.objects.all()
      context = {'users': users}
      return render(request, 'accounts/index.html', context)
  
  
  def detail(request, user_pk):
      user = get_object_or_404(User, pk=user_pk)
      context = {'user': user}
      return render(request, 'accounts/detail.html', context)
  
  ```

- templates/accounts/index.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}사람들{% endblock title %}
  
  {% block content %}
  {% for user in users %}
  {{ user.id }}. <a href="{% url 'accounts:detail' user.id %}">{{ user.username }}</a>
  {% endfor %}
  {% endblock content %}
  
  ```

- templates/accounts/detail.html

  - 우선 빈페이지로 만들기

  ```django
  {% extends 'base.html' %}
  
  {% block title %}사람{% endblock title %}
  
  {% block content %}
  
  {% endblock content %}
  ```

  

#### 실컷 만들었는데 회원가입, 로그인, 로그아웃을 확인하도록 base.html 을 수정하자



#### 4.5. pjt10/base.html

```django
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <script src="https://kit.fontawesome.com/58a4b12f94.js" crossorigin="anonymous"></script>
  <title>{% block title %}{% endblock %}</title>
</head>
<body>
  {% if user.is_authenticated %}
  <a href="{% url 'accounts:logout' %}">[LOGOUT]</a>
  {% else %}
  <a href="{% url 'accounts:login' %}">[LOGIN]</a>
  <a href="{% url 'accounts:signup' %}">[SIGNUP]</a>
  {% endif %}
  <br>
  <hr>
  
  {% block content %}{% endblock %}  
</body>
</html>

```



#### accounts app 작업은 일단 마무리 짓고 movies app 고고!



---

### 5. movies app

- 기능구현에 앞서, 우린 현재 데이터가 없기 때문에 admin 페이지로 접근해서 데이터를 수동으로 넣어보자!
- why? 명세에 `Genre와 영화는 생성/수정/삭제를 만들지 않습니다.`가 있기 때문!

```bash
$ python manage.py createsuperuser

```

- 서버 켜서 admin/으로 접근 하고, 로그인 해서 Movie에 정보 넣기

- 구현해야할 기능

  - 영화목록조회, 영화상세보기, 평점생성, 평점삭제, 영화 좋아요 기능

    

#### 5.1. 영화목록 조회기능 구현

- 영화 이미지 클릭하면 상세보기 페이지로 넘어가도록 만들자!

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
  ]
  
  ```

- views.py

  ```python
  from django.shortcuts import render, redirect, get_object_or_404
  from django.views.decorators.http import require_POST, require_GET
  from django.contrib.auth.decorators import login_required
  from django.http import HttpResponse, JsonResponse
  from .models import Movie, Review, Genre
  from .forms import ReviewForm
  from  accounts.models import User
  
  
  def index(request):
      movies = Movie.objects.all()
      context = { 'movies': movies }
      return render(request, 'movies/index.html', context)
  
  ```

- templates/movies/index.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}시작{% endblock title %}
  
  {% block content %}
  {% for movie in movies %}
  {{ movie.title }}
  <a href="{% url 'movies:detail' movie.id %}">{{ movie.poster_url }}</a>
  {% endfor %}
  {% endblock content %}
  
  ```



#### 5.2. 영화 상세보기 기능 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:movie_pk>/', views.detail, name='detail'),
      
  ```

- views.py

  ```python
  @require_GET
  def detail(request, movie_pk):
      movie = get_object_or_404(Movie, pk=movie_pk)
      reviews = movie.reviews.all()
      form = ReviewForm()
      context = {
          'movie': movie,
          'reviews': reviews,
          'form': form,
      }
      return render(request, 'movies/detail.html', context)
  
  ```

- templates/movies/detail.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}영화 상세정보{% endblock title %}
  
  {% block content %}
  <p>
    {{ movie.title }}
    {{ movie.audience }}
    {{ movie.description }}
  </p><hr>
  
  {% endblock content %}
  
  ```

  

#### 5.3. 평점생성 기능구현

- 리뷰 작성할 form을 만들기 위해 forms.py 파일 생성하자

  ```python
  from django import forms
  from .models import Review
  
  
  class ReviewForm(forms.ModelForm):
      content = forms.CharField(
          label='리뷰',
      )
  
      class Meta:
          model = Review
          fields = ['content', 'score']
  
  ```

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:movie_pk>/', views.detail, name='detail'),
      path('<int:movie_pk>/reviews/new/', views.create_review, name='create_review'),
      
  ```

- views.py

  ```python
  @require_POST
  def create_review(request, movie_pk):
      movie = get_object_or_404(Movie, pk=movie_pk)
      if request.user.is_authenticated:
          form = ReviewForm(request.POST)
          if form.is_valid():
              review = form.save(commit=False)
              review.movie_id = movie_pk
              review.user = request.user
              review.save()
      return redirect('movies:detail', movie_pk)
  
  ```

- templates/movies/detail.html

  - **유의! 로그인 된 사람만 평점 남길 수 있음!!**

  ```django
  {% extends 'base.html' %}
  
  {% block title %}영화 상세정보{% endblock title %}
  
  {% block content %}
  <p>
    {{ movie.title }}
    {{ movie.audience }}
    {{ movie.description }}
  </p><hr>
  
  {% for review in reviews %}
  <p>
    {{ review.content }}
    {{ review.score }}
  </p><hr>
  {% endfor %}
  
  {% if user.is_authenticated %}
  <form action="{% url 'movies:create_review' movie.pk %}", method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn-warning" type="submit">Review Create</button>
  </form>
  {% endif %}
  {% endblock content %}
  ```



#### 5.4. 평점 삭제 기능 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:movie_pk>/', views.detail, name='detail'),
      path('<int:movie_pk>/reviews/new/', views.create_review, name='create_review'),
      path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
  ]
  
  ```

- views.py

  ```python
  @require_POST
  def delete_review(request, movie_pk, review_pk):
      if request.user.is_authenticated:
          review = get_object_or_404(Review, pk=review_pk)
          movie = get_object_or_404(Movie, pk=movie_pk)
          if review.user == request.user or movie.user == request.user:   
              review.delete()
          return redirect('movies:detail', movie_pk)
      
  ```

- templates/movies/detail.html

  - **유의! 평점 남긴 유저만 자신의 글을 지울 수 있음!!**

  ```django
  {% extends 'base.html' %}
  
  {% block title %}영화 상세정보{% endblock title %}
  
  {% block content %}
  <p>
    {{ movie.title }}
    {{ movie.audience }}
    {{ movie.description }}
  </p><hr>
  
  <a href="{% url 'movies:like' movie.pk %}">
    {% if user in movie.liked_users.all %}
    <i class="fas fa-heart fa-lg" style="color: pink"></i>
    {% else %}
    <i class="far fa-heart fa-lg" style="color: pink"></i>
    {% endif %}
  </a>
  <span id="like-count">{{ movie.liked_users.all | length }}</span>명이 이 글을 좋아합니다.
  
  
  {% for review in reviews %}
  <p>
    {{ review.content }}
    {{ review.score }}
    {% if review.user == request.user %}
    <form action="{% url 'movies:delete_review' movie.pk review.pk %}", method="POST">
      {% csrf_token %}
      <button class="btn btn-link" type="submit">Review Delete</button>
    </form>
    {% endif %}
  </p><hr>
  {% endfor %}
  
  {% if user.is_authenticated %}
  <form action="{% url 'movies:create_review' movie.pk %}", method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn-warning" type="submit">Review Create</button>
  </form>
  {% endif %}
  {% endblock content %}
  
  ```



#### 5.5. 영화 좋아요 기능 구현

- urls.py

  ```python
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:movie_pk>/', views.detail, name='detail'),
      path('<int:movie_pk>/reviews/new/', views.create_review, name='create_review'),
      path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
      path('<int:movie_pk>/like/', views.like, name='like'),
  ]
  
  ```

- views.py

  ```python
  @login_required
  def like(request, movie_pk):
      user = request.user
      movie = get_object_or_404(Movie, pk=movie_pk)
      # exists 한개의 데이터라도 존재하면 true
      if movie.liked_users.filter(pk=user.pk).exists():
      # if user in movie.liked_users.all():
          user.liked_movies.remove(movie)
          liked = False 
      else:
          user.liked_movies.add(movie)
          liked = True
      context = {
          'liked': liked, 
          'count': movie.liked_users.count()
      }
      return redirect('movies:detail', movie_pk)
  
  ```

- templates/movies/detail.html

  - fontawesome 활용

  ```django
  {% extends 'base.html' %}
  
  {% block title %}영화 상세정보{% endblock title %}
  
  {% block content %}
  <p>
    {{ movie.title }}
    {{ movie.audience }}
    {{ movie.description }}
  </p><hr>
  
  <a href="{% url 'movies:like' movie.pk %}">
    {% if user in movie.liked_users.all %}
    <i class="fas fa-heart fa-lg" style="color: pink"></i>
    {% else %}
    <i class="far fa-heart fa-lg" style="color: pink"></i>
    {% endif %}
  </a>
  <span id="like-count">{{ movie.liked_users.all | length }}</span>명이 이 글을 좋아합니다.
  
  
  {% for review in reviews %}
  <p>
    {{ review.content }}
    {{ review.score }}
    {% if review.user == request.user %}
    <form action="{% url 'movies:delete_review' movie.pk review.pk %}", method="POST">
      {% csrf_token %}
      <button class="btn btn-link" type="submit">Review Delete</button>
    </form>
    {% endif %}
  </p><hr>
  {% endfor %}
  
  {% if user.is_authenticated %}
  <form action="{% url 'movies:create_review' movie.pk %}", method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn-warning" type="submit">Review Create</button>
  </form>
  {% endif %}
  {% endblock content %}
  
  ```

  

#### 다 끝났나..? 응 아니야^^ 아까 pass했던 accounts/detail/ 작업하러 가자

---

### 6. 마무리 작업



#### 6.1. accounts app

- templates/accounts/detail.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}사람{% endblock title %}
  
  {% block content %}
  {% for review in user.reviews.all %}
  {{ review.content }} {{ review.score }}
  {% endfor %}
  
  {% for movie in user.liked_movies.all %}
  {{ movie.title }}
  {% endfor %}
  
  {% endblock content %}
  
  ```

- 그런데, 여기서 문제! 명세에 있던 `해당 유저를 팔로우 한 사람의 수, 팔로인 한 사람의 수`를 출력해야 한다..!

  - **[문제] 영화 생성 페이지를 구현하지 않아 작성자를 팔로우할 수도 없는데 어떻게 해야할 지 고민이 되었음**

  - [접근] 리뷰작성자를 찾아 팔로우 하는 식으로 로직을 짬

    

#### 6.2. follow 기능 구현

- movies/urls.py

  ```python 
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  urlpatterns = [
      path('', views.index, name='index'),
      path('<int:movie_pk>/', views.detail, name='detail'),
      path('<int:movie_pk>/reviews/new/', views.create_review, name='create_review'),
      path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
      path('<int:movie_pk>/like/', views.like, name='like'),
      path('<int:movie_pk>/<int:review_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
  ]
  
  ```

- movies/views.py

  ```python
  @login_required
  def follow(request, movie_pk, review_pk, user_pk):
      # 로그인한 유저가 게시글 유저를 Follow or unfollow 한다. 
      user = request.user
      person = get_object_or_404(User, pk=user_pk)
  
      if user in person.followers.all(): # 이미 팔로워다
          person.followers.remove(user) # 언팔 
      else:
          person.followers.add(user) # 팔로우함
  
      return redirect('movies:detail', movie_pk)
  
  ```

- movies/templates/movies/detail.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}영화 상세정보{% endblock title %}
  
  {% block content %}
  <p>
    {{ movie.title }}
    {{ movie.audience }}
    {{ movie.description }}
  </p><hr>
  
  <a href="{% url 'movies:like' movie.pk %}">
    {% if user in movie.liked_users.all %}
    <i class="fas fa-heart fa-lg" style="color: pink"></i>
    {% else %}
    <i class="far fa-heart fa-lg" style="color: pink"></i>
    {% endif %}
  </a>
  <span id="like-count">{{ movie.liked_users.all | length }}</span>명이 이 글을 좋아합니다.
  
  {% for review in reviews %}
  <p>
    {{ review.content }}
    {{ review.score }}
    {% if user != review.user %}
      {% if user in movie.user.followers.all %}
      <a href="{% url 'movies:follow' movie.pk review.pk review.user.pk %}" class="btn btn-primary btn-lg">Unfollow</a>
      {% else %}
      <a href="{% url 'movies:follow' movie.pk review.pk review.user.pk %}" class="btn btn-primary btn-lg">Follow</a>
      {% endif %} 
    {% endif %}
    {% if review.user == request.user %}
    <form action="{% url 'movies:delete_review' movie.pk review.pk %}", method="POST">
      {% csrf_token %}
      <button class="btn btn-link" type="submit">Review Delete</button>
    </form>
    {% endif %}
  </p><hr>
  {% endfor %}
  
  {% if user.is_authenticated %}
  <form action="{% url 'movies:create_review' movie.pk %}", method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn-warning" type="submit">Review Create</button>
  </form>
  {% endif %}
  {% endblock content %}
  
  ```

- accounts/templates/accounts/detail.html

  ```django
  {% extends 'base.html' %}
  
  {% block title %}사람{% endblock title %}
  
  {% block content %}
  {% for review in user.reviews.all %}
  {{ review.content }} {{ review.score }}
  {% endfor %}
  
  {% for movie in user.liked_movies.all %}
  {{ movie.title }}
  {% endfor %}
  
  
  팔로잉 : {{ user.followings.all | length }} / 팔로워 : {{ user.followers.all | length }}
  
  {% endblock content %}
  
  ```



#### Finally, PJT 10 끝!!!!



---

### 에필로그(PJT10을 마치고..)



- 복붙도 잘해야 복붙한다
- 협업을 함에있어 소통의 중요성을 깊이 깨달음
- 협업도구로서의 git을 사용하는 것이 매우 번거로움을 느낌
- 분담을 잘 해야 프로젝트 효율성을 높일 수 있음을 깨달음
- 화내지말고 짜증내지말고 긍정적인 마인드로 즐코하자!

 