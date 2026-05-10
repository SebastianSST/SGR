from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

@login_required
def dashboard(request):
    user_type = request.user.user_type
    context = {
        'user_type': user_type,
        'user': request.user,
    }
    
    if user_type == 'admin':
        return render(request, 'authentication/admin_dashboard.html', context)
    elif user_type == 'waiter':
        return render(request, 'authentication/waiter_dashboard.html', context)
    else:
        return render(request, 'authentication/client_dashboard.html', context)

def home(request):
    return render(request, 'authentication/home.html')
