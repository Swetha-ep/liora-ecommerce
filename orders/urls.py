from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('buy_now/', views.buy_now, name='buy_now'),

]
