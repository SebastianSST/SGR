from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'authentication/home.html')

def dashboard(request):
    # Simulate admin user for demo purposes
    context = {
        'user_type': 'admin',
        'user': {'username': 'admin', 'user_type': 'admin'},
    }
    return render(request, 'authentication/admin_dashboard.html', context)

def menu_dashboard(request):
    context = {
        'user_type': 'client',
        'user': {'username': 'guest', 'user_type': 'client'},
    }
    return render(request, 'authentication/client_dashboard.html', context)

def orders_dashboard(request):
    context = {
        'user_type': 'waiter',
        'user': {'username': 'waiter', 'user_type': 'waiter'},
    }
    return render(request, 'authentication/waiter_dashboard.html', context)
