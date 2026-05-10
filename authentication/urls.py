from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('menu/', views.menu_dashboard, name='menu_dashboard'),
    path('orders/', views.orders_dashboard, name='orders_dashboard'),
]
