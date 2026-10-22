from django.urls import path
from .views import *



urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/holidays/', dashboard_holidays, name='dashboard_holidays'),
]