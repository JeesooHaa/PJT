from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.movies, name='movies'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    path('<int:movie_pk>/reviews/', views.reviews, name='reviews'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:comment_pk>/commentupdate/', views.commentupdate, name='commentupdate'),
    path('<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
]
