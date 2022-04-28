'''
URLs for the endpoints are stored in this file
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input', views.input_title, name='input_title'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('annotate/<int:pk>', views.annotate, name='annotate'),
    path('dashboard', views.dashboard, name='dashboard'),
]
