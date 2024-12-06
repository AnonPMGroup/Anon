from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Product, Category
from django.urls import reverse


def user_profile(request):
    user = request.user
    categories = Category.objects.all()
    return render(request, 'store/profile.html', {'user': user, 'categories': categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()  
    categories = Category.objects.all()
    return render(request, 'store/category_detail.html', {'category': category, 'products': products, 'categories': categories})


def product_list(request):
    products = Product.objects.all()

    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    return render(request, 'store/product_detail.html', {'product': product, "categories": categories})


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
        categories = Category.objects.all()
        return render(request, 'store/index.html', {'user': request.user, 'categories': categories})