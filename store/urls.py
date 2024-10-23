from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('register/', register_view, name='register'), 
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', index, name='home'),
]