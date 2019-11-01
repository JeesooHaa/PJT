from django.urls import path
from . import views
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
    path('genres/', views.genres, name='genres'),
    path('genres/<int:genre_pk>/', views.genres_list, name='genres_list'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_pk>/reviews/', views.movie_review_create, name='movie_review_create'),
    path('reviews/<int:review_pk>/', views.review_detail_update_delte, name='review_detail_update_delte'),

    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
]
