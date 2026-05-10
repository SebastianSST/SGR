from django.urls import path
from . import views

app_name = 'cash'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('open/', views.open_register, name='open_register'),
    path('close/', views.close_register, name='close_register'),
    path('daily-report/', views.daily_report, name='daily_report'),
    path('history/', views.register_history, name='register_history'),
    path('export/', views.export_daily_report, name='export_report'),
]
