from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('products/',views.products,name='products'),
]
