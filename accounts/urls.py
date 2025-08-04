
from django.urls import path
from . import views

urlpatterns = [
    path('auth_page/', views.auth_page, name='auth_login'),
    path('logout/', views.logout_view, name='auth_logout'),
    path('profile/',views.profile,name='profile'),
    path('add_address/',views.add_address,name='add_address'),
]
