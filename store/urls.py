from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('register/', register_view, name='register'), 
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', index, name='home'),
    # Category
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),

    # Product
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

    path('profile/', user_profile, name='user-profile'),
    path('cart/', cart_detail, name='cart-detail'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove-from-cart'),
    path('cart/increase/<int:product_id>/', increase_quantity_view, name='increase-quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity_view, name='decrease-quantity'),
    path('favorites/toggle/<int:product_id>/', toggle_favorite, name='toggle-favorite'),
    path('favorites/', favorite_list, name='favorite-list'),
]