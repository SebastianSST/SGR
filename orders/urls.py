from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/update-status/', views.update_order_status, name='update_status'),
    path('<int:pk>/take/', views.take_order, name='take_order'),
    path('kitchen/', views.kitchen_orders, name='kitchen_orders'),
]
