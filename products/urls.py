from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('products/<slug:slug>/',views.products,name='products'),
    path('product_view/<slug:slug>/', views.product_view, name='product_view'),
]
