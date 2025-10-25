from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    
    path('products/<slug:slug>/',views.products,name='products'),
    path('product_view/<slug:slug>/', views.product_view, name='product_view'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_remove/<int:inventory_id>/', views.wishlist_remove, name='wishlist_remove'),

    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
]

