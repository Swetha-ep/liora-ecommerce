from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('products_list/', views.products_list, name='products_list'),
    path('add_products/', views.add_products, name='add_products'),
    path('category_list/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<pk>/', views.delete_category, name='delete_category'),
]
