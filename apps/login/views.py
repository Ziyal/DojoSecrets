from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import re
import bcrypt
password = "kittens"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login/index.html')

def register(request):
    if request.method == "POST":
        validation = User.objects.regVal(request.POST)

        if validation[0]:
            request.session['current_user']=validation[1].first_name
            request.session['user_id']=validation[1].id
            return redirect("wall:index")
        else:
            for error in validation[1]:
                messages.error(request, error)
            return redirect('/')
    return redirect('/')

def login(request):
    if request.method == "POST":
        validation = User.objects.logVal(request.POST)

        if validation[0]:
            request.session['current_user']=validation[1].first_name
            request.session['user_id']=validation[1].id
            return redirect("wall:index")
        else:
            for error in validation[1]:
                messages.error(request, error)
            return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
