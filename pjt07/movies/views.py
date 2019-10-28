from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from django.contrib.auth.models import User


def movies(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/movies.html', context)


def create(request):
    if request.user.is_authenticated:
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


def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = MovieForm(instance=movie)
    context = {'form': form}
    return render(request, 'movies/update.html', context)


@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect('movies:movies')


@require_POST
def reviews(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie_id = movie_pk
            comment.user = request.user
            comment.save()
    return redirect('movies:detail', movie_pk)


def commentupdate(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user_pk = comment.user_id
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', user_pk)
    else:
        user = User.objects.get(pk=user_pk)
        movies = user.liked_movies.all()
        comments = user.comment_set.all()
        form = CommentForm(instance=comment)
        context = {
            'user': user,
            'movies': movies,
            'comments': comments,
            'form': form,
            'comment_pk': comment_pk,
        }
        return render(request, 'accounts/detail.html', context)
    #     form = MovieForm(instance=movie)
    # context = {'form': form}
    # return render(request, 'movies/update.html', context)


@require_POST
def comment_delete(request,comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    movie_pk = comment.movie_id
    if comment.user == request.user:
        comment.delete()
    return redirect('movies:detail',movie_pk)


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
