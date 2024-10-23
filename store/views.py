from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'store/login.html')  

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('login')  
    return render(request, 'store/register.html')  



def index(request):
    if request.user.is_authenticated:
        return render(request, 'store/index.html', {'user': request.user})