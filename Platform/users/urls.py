#users/urls.py

"""
URL configuration for the users app.

This module defines the URL patterns for the users app, mapping URLs to views for user authentication and registration.

URL Patterns:
    login (path): URL pattern for the user login view.
    logout (path): URL pattern for the user logout view.
    register (path): URL pattern for the user registration view.

"""


from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register_user,name='register'),
]
