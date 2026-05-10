from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('create/', views.reservation_create, name='reservation_create'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/edit/', views.reservation_edit, name='reservation_edit'),
    path('<int:pk>/cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('<int:pk>/confirm/', views.reservation_confirm, name='reservation_confirm'),
    path('tables/', views.table_list, name='table_list'),
    path('tables/create/', views.table_create, name='table_create'),
    path('calendar/', views.calendar_view, name='calendar'),
]
