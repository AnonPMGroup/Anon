from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse


def get_user_favorites(user):
    return Favorite.objects.filter(user=user).select_related('product')

def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def favorite_list(request):
    favorites = get_user_favorites(request.user)
    return render(request, 'store/favorite_list.html', {'favorites': favorites})

def get_last_four_products():
    return Product.objects.order_by('-created_at')[:4]

def increase_quantity_view(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart-detail')

def decrease_quantity_view(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    if cart_item.quantity > 1:  
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete() 
    return redirect('cart-detail')

def add_to_cart(user, product_id, quantity=1):
    cart, created = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += quantity
    cart_item.save()

def remove_from_cart(user, product_id):
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.delete()

def update_cart_item(user, product_id, quantity):
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.quantity = quantity
    cart_item.save()

def clear_cart(user):
    cart = Cart.objects.get(user=user)
    cart.items.all().delete()

def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'store/cart_detail.html', {'cart': cart})

def add_to_cart_view(request, product_id):
    add_to_cart(request.user, product_id)
    return redirect('cart-detail')

def remove_from_cart_view(request, product_id):
    remove_from_cart(request.user, product_id)
    return redirect('cart-detail')

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
    favorites = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    return render(request, 'store/category_detail.html', {'category': category, 'products': products, 'categories': categories, 'favorites': favorites})


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
        return render(request, 'store/index.html', {'user': request.user, 'categories': categories, 'new_arrivals': get_last_four_products()})