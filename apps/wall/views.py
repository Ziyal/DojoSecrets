from django.shortcuts import render, redirect
from .models import Secret
from django.contrib import messages
from ..login.models import User
from django.db.models import Count

def index(request):
    if not "current_user" in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('login:index')

    context = {
        "users": User.objects.all,
        "secrets": Secret.objects.annotate(num_likes=Count('like')).order_by('-created_at'),
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'wall/index.html', context)

def add_secret(request):
    if request.method == "POST":
        new_post = Secret.objects.process_secret(request.POST, request.session['user_id'])
        print new_post.post
        return redirect('wall:index')

def add_like(request):
    if request.method == "POST":
        user_likes = Secret.objects.process_like(request.POST)
        return redirect('wall:index')
        # if request.POST["page"] == "1":
        #     return redirect('wall:index')
        # else:
        #     return redirect('wall:most_popular')

def add_like2(request):
    if request.method == "POST":
        user_likes = Secret.objects.process_like(request.POST)
        return redirect('wall:most_popular')

def most_popular(request):
    if not "current_user" in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('login:index')
    context = {
        "users": User.objects.all,
        "current_user": User.objects.get(id=request.session['user_id']),
        "secrets":Secret.objects.annotate(num_likes=Count('like')).order_by('-num_likes')
    }
    return render(request, 'wall/most_popular.html', context)

def delete_secret(request):
    post_to_delete = Secret.objects.get(id=request.POST['secret_id'])
    post_to_delete.delete()
    return redirect('wall:index')

def delete_secret2(request):
    post_to_delete = Secret.objects.get(id=request.POST['secret_id'])
    post_to_delete.delete()
    return redirect('wall:most_popular')

def logout(request):
    request.session.clear()
    return redirect('login:index')
