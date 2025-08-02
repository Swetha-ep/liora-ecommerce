from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('auth_page/', views.auth_page, name='auth_login'),
    path('logout/', views.logout_view, name='auth_logout'),
    path('add_address/',views.ajax_add_address,name='add_address'),
]
