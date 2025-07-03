from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('products_list/', views.products_list, name='products_list'),
    path('add_products/', views.add_products, name='add_products'),
    path('category_list/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
]
