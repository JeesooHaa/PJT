from django.urls import path
from . import views

# articles/____
urlpatterns = [
    path('', views.movies),
    path('new/', views.new),
    path('create/', views.create),
    path('<int:movie_pk>/', views.detail),
    path('<int:movie_pk>/edit/', views.edit),
    path('<int:movie_pk>/update/', views.update),
    path('<int:movie_pk>/delete/', views.delete),
]
