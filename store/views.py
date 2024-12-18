from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg
from random import sample


def get_random_products():
    products = list(Product.objects.all()) 
    return sample(products, min(len(products), 4)) 

def get_top_rated_products():
    return Product.objects.annotate(average_rating=Avg('ratings__rating')).order_by('-average_rating')[:4]

def rate_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user_rating = int(request.POST.get('rating')) 
        user_rating = max(1, min(user_rating, 5)) 

        rating, created = Rating.objects.get_or_create(user=request.user, product=product)
        rating.rating = user_rating
        rating.save()

        return redirect('product-detail', pk=product.id)

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
    categories = Category.objects.all()
    return render(request, 'store/favorite_list.html', {'favorites': favorites, 'categories': categories})

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
    categories = Category.objects.all()
    return render(request, 'store/cart_detail.html', {'cart': cart, 'categories': categories})

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
    recently_viewed_products = None
    if 'recently_viewed' in request.session:
        if pk in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(pk)

        products = Product.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(products,
                                          key=lambda x: request.session['recently_viewed'].index(x.id)
                                          )
        request.session['recently_viewed'].insert(0, pk)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [pk]

    request.session.modified = True
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    if user_rating:
        user_rating = user_rating.rating
    return render(request, 'store/product_detail.html', 
                  {'product': product,
                    "categories": categories,
                      'recently_viewed_products': recently_viewed_products,
                        'user_rating': user_rating or 0})


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
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        errors = []

        try:
            validate_email(email)
        except ValidationError:
            errors.append("Enter a valid email address.")

        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")

        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)

        if password != confirm_password:
            errors.append("Passwords do not match.")

        if errors:
            return render(request, 'store/register.html', {'errors': errors})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )
        user.save()
        return redirect('login')

    return render(request, 'store/register.html')



def index(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        return render(request, 'store/index.html', {'user': request.user, 'categories': categories,
                                                     'new_arrivals': get_last_four_products(), 'top_rated': get_top_rated_products(),
                                                     "trending": get_random_products()})