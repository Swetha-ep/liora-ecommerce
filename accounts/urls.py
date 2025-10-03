
from django.urls import path
from . import views

urlpatterns = [
    path('auth_page/', views.auth_page, name='auth_login'),
    path('logout/', views.logout_view, name='auth_logout'),

    path('profile/',views.profile,name='profile'),
    path('add_address/',views.add_address,name='add_address'),
    
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<str:token>/", views.reset_password, name="reset_password"),
]
