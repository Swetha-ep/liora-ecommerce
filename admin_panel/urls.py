from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('products_list/', views.products_list, name='products_list'),
]
