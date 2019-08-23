from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'audience', 'open_date', 'genre', 'watch_grade', 'score', 'poster_url', 'description',)
