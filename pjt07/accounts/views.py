from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from movies.forms import CommentForm


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/index.html', context)


def detail(request, user_pk):
    user = User.objects.get(pk=user_pk)
    movies = user.liked_movies.all()
    comments = user.comment_set.all()
    context = {
        'user': user,
        'movies': movies,
        'comments': comments
    }
    return render(request, 'accounts/detail.html', context)
    
    # user = User.objects.get(pk=user_pk)
    # movies = user.liked_movies.all()
    # comments = user.comment_set.all()
    # if request.method == 'POST':
    #     form = CommentForm()
    #     context = {
    #         'user': user,
    #         'movies': movies,
    #         'comments': comments,
    #         'form': form, 
    #     }
    # else:
    #     context = {
    #         'user': user,
    #         'movies': movies,
    #         'comments': comments
    #     }
    # return render(request, 'accounts/detail.html', context)


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


def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_page = request.GET.get('next')
            return redirect(next_page or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:index')
