#### 2019-10-28 (월)

# Project 07 

Project 06 의 내용을 확장하여 인증 기능을 구현한다. 

## Accounts App

유저의 회원가입과 로그인, 로그아웃 기능을 구현한다. 

1. 유저 목록 ( /accounts/ ) 
   
   1. (필수) 사용자의 목록이 나타나며, 사용자의 username 을 클릭하면 유저 상세보기 페이지로 넘어 갑니다. 
   
      ```
      def index(request):
          users = User.objects.all()
          context = {'users': users}
          return render(request, 'accounts/index.html', context)
      ```
   
      ```html
      {% extends 'base.html' %}
      
      {% block title %}
      {% endblock title %}
      
      
      {% block content %}
      {% for user in users %}
      <a href="{% url 'accounts:detail' user.pk %}">{{ user.username }}</a>
      
      {% endfor %}
      {% endblock %}
      ```
   
      
   
2. 유저 상세보기 ( /accounts/{user_pk}/ ) 
   1. (필수) 해당 유저가 작성한 평점 정보가 모두 출력됩니다.
   
   2. (필수) 해당 유저가 좋아하는 평점 정보가 모두 출력됩니다. 
   
   3. (선택) 각각 평점을 수정할 수 있도록 구성합니다. 
   
      ```python
      def detail(request, user_pk):
          user = User.objects.get(pk=user_pk)
          movies = user.liked_movies.all()
          comments = user.comment_set.all()
          if request.method == 'POST':
              form = CommentForm()
              context = {
                  'user': user,
                  'movies': movies,
                  'comments': comments,
                  'form': form, 
              }
          else:
              context = {
                  'user': user,
                  'movies': movies,
                  'comments': comments
              }
          return render(request, 'accounts/detail.html', context)
      
      ```
   
      ```html
      {% extends 'base.html' %}
      
      {% block title %}상세보기( ͡° ͜ʖ ͡°){% endblock title %}
      
      
      {% block content %}
      <h3>좋아하는 영화 목록</h3>
      {% for movie in movies  %}
      <p>{{ movie.title }}의 평점: {{ movie.score }}점</p>
      {% endfor %}
      
      <hr>
      <h3>코멘트를 단 영화 목록</h3>
      {% for comment in comments %}
      <p>{{ comment.movie.title }}</p>
      <p>{{ comment.content }}</p>
      <p>{{ comment.score }}</p>
      {% if form %}
      <form action="{% url 'movies:commentupdate' comment.pk %}" method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">[수정]</button>
      </form>
      {% else %}
      <form action="{% url 'accounts:detail' user.pk %}" method="POST">
      {% csrf_token %}
      {% comment %} <form action="{% url 'movies:commentupdate' comment.pk %}"> {% endcomment %}
      <button type="submit">[수정하기]</button>
      </form>
      {% endif %}
      <hr>
      {% endfor %}
      {% endblock content %}
      ```
   
      
   
3. 유저 회원가입 ( /accounts/signup/ )
   
   1. (필수) UserCreationForm 을 사용하여 회원가입 기능을 구현합니다.
   
      ```python
      def signup(request):
          if request.user.is_authenticated:
              return redirect('accounts:index')
          if request.method == 'POST':
              form = UserCreationForm(request.POST)
              if form.is_valid():
                  user = form.save()
                  auth_login(request, user)
                  return redirect('accounts:index')
          else:
              form = UserCreationForm()
          context = {'form': form}
          return render(request, 'accounts/signup.html', context)
      ```
   
      ```html
      {% extends 'base.html' %}
      
      {% block title %}상세보기( ͡° ͜ʖ ͡°){% endblock title %}
      
      
      {% block content %}
      여기 
      <form method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">[SUBMIT]</button>
      </form>
      
      {% endblock content %}
      ```
   
      
   
      
   
4. 유저 로그인 (/accounts/login/)
   
   1. (필수) AuthenticationForm 을 사용하여 로그인 기능을 구현합니다.
   
      ```python
      def login(request):
          if request.user.is_authenticated:
              return redirect('accounts:index')
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
   
      ```html
      {% extends 'base.html' %}
      
      {% block title %}상세보기( ͡° ͜ʖ ͡°){% endblock title %}
      
      
      {% block content %}
      <form method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">[SUBMIT]</button>
      </form>
      
      {% endblock content %}
      ```
   
      
   
5. 유저 로그아웃 ( /accounts/logout/ )
   
   1. (필수) 로그아웃을 구현합니다.
   
      ```python
      def logout(request):
          auth_logout(request)
          return redirect('accounts:index')
      ```
   
      

## Movies App

1. 영화 상세보기 ( /movies/{movie_pk} )
   1. (필수) 로그인 한 사람만 영화 평점을 남길 수 있습니다.
   
2. (필수) 모든 사람은 평점 목록을 볼 수 있습니다.
   
      ```python
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
   
      ```html
      {% extends 'base.html' %}
      
      {% block title %}{{ movie.title }}{% endblock title %}
      
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
      
      ...
      
      {% endblock %}
      ```
   
      
   
2. 영화 생성 ( /movies/ )
   
1. (필수) 로그인 한 사람만 영화를 생성할 수 있습니다.
   
      ```python
      def create(request):
          if request.user.is_authenticated: # 로그인 한 사람만 
              if request.method == 'POST':
                  form = MovieForm(request.POST)
                  if form.is_valid():
                      movie = form.save()
                      return redirect('movies:detail', movie.pk)
              else:
                  form = MovieForm()
              context = {'form': form}
              return render(request, 'movies/create.html', context)
          return redirect('movies:index')
      ```
   
      ```html
      {% extends 'base.html' %}
      {% comment %} {% load bootstrap4 %} {% endcomment %}
      
      {% block title %}Movie::Create{% endblock title %}
      
      {% block content %}
      <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        {% comment %} {% bootstrap_form form layout='horizontal' %} {% endcomment %}
        <button type="submit">SUBMIT</button>
      </form>
      {% endblock %}
      ```
   
      
   
      
   
3. 평점 생성
   
1. (필수) 영화 평점은 로그인 한 사람만 남길 수 있습니다.
   
      ```python
      def reviews(request, movie_pk):
          if request.user.is_authenticated:	# 로그인한사람만
              movie = get_object_or_404(Movie, pk=movie_pk)
              form = CommentForm(request.POST)
              if form.is_valid():
                  comment = form.save(commit=False)
                  comment.movie_id = movie_pk
                  comment.user = request.user
                  comment.save()
          return redirect('movies:detail', movie_pk)
      ```
   
      
   
4. 평점 삭제
   
1. (필수) 평점 삭제는 본인만 가능합니다.
   
      ```python
      @require_POST
      def comment_delete(request,comment_pk):
          comment = get_object_or_404(Comment, pk=comment_pk)
          movie_pk = comment.movie_id
          if comment.user == request.user:
              comment.delete()
          return redirect('movies:detail',movie_pk)
      ```
   
      ```html
      {% block content %}
        ...
      
        {% for comment in comments %}
          <p>{{ comment.pk }}. {{ comment.content }} {{ comment.score }}</p>
          <form action="{% url 'movies:comment_delete' comment.pk %}" method="POST">
            {% csrf_token %}
            <button type="submit">DELETE</button>
          </form>
        {% endfor %}
      ```
   
      
   
5. 영화 좋아요 기능 구현
   1. (필수) 좋아하는 영화를 담아 놓을 수 있도록 구현합니다.
   
   2. (필수) 로그인 한 유저만 해당 기능을 사용할 수 있습니다.
   
   3. (필수)  영화 좋아요 URL은 POST /movies/1/like/ 등 이며, 동적으로 할당되는 부분이 존재합니다. 동적으로 할당되는 부분에는 데이터베이스에 저장된 영화 정보의 Primary Key가 들어갑니다.
   
   4. (필수) 적합한 위치에 좋아요 링크를 생성합니다.
   
   5. (필수) 영화가 존재 하지 않는 경우 404 페이지를 보여줍니다.
   
      ```python
      @require_POST
      def like(request, movie_pk):
          movie = get_object_or_404(Movie, pk=movie_pk)
          user = request.user
          if user.is_authenticated:
              if user in movie.liked_users.all():
                  user.liked_movies.remove(movie)
              else:
                  user.liked_movies.add(movie)
          return redirect('movies:detail', movie_pk)
      ```
   
      ```html
      {% block content %}
      
        <form action="{% url 'movies:like' movie.pk %}" method="POST">
        {% csrf_token %}
        <button type="submit">[좋아요]</button>
        </form>
        {{ movie.liked_users.all | length }} 명이 좋아합니다.
      ...
      
      {% endblock %}
      
      ```
   
      

