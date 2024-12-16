from .models import *
from django.db import models


def get_cart_item_count(user):
    try:
        cart = Cart.objects.get(user=user)
        total_items = cart.items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
        return total_items
    except Cart.DoesNotExist:
        return 0

def cart_item_count(request):
    if request.user.is_authenticated:
        return {'cart_item_count': get_cart_item_count(request.user)}
    return {'cart_item_count': 0}

def get_fav_item_count(user):
    try:
        return Favorite.objects.filter(user=user).count()
    except Favorite.DoesNotExist:
        return 0
    

def fav_item_count(request):
    if request.user.is_authenticated:
        return {'fav_item_count': get_fav_item_count(request.user)}
    return {'fav_item_count': 0}