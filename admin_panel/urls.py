from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('products_list/', views.products_list, name='products_list'),
    path('add_products/', views.add_products, name='add_products'),

    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('add_category/', views.CategoryCreate.as_view(), name='add_category'),
    path('edit_category/<pk>/', views.CategoryUpdate.as_view(), name='edit_category'),
    path('delete_category/<pk>/', views.CategoryDelete.as_view(), name='delete_category'),
]
