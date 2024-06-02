#users/views.py

"""
User authentication views for login, logout, and registration.

Functions:
    login_user(request):
        Handle user login. If the request method is POST, authenticate the user and log them in.
        If authentication fails, redirect to the login page with an error message.
        If the request method is GET, render the login page.

    logout_user(request):
        Log out the current user and redirect to the home page with a success message.

    register_user(request):
        Handle user registration. If the request method is POST, validate and save the user form.
        Authenticate and log in the new user, then redirect to the index page with a success message.
        If the request method is GET, render the registration page with an empty form.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('app:index')
        else:
            messages.success(request, "There was an error logging in, please try again.")
            return redirect('users:login')
    else:
        return render(request, 'authenticate/login.html',{})
    

def logout_user(request):
    logout(request)
    messages.success(request,"You were logged out.")
    return redirect ('app:home')

def register_user(request):
    if request.method == "POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successfull!")
            return redirect('app:index')
    else:
            form=UserCreationForm()
            username= " # Initialize username for the context"
        
    return render(request,'authenticate/register.html',{
            'form':form
    })
