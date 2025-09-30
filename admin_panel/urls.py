from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    
    path('products_list/', views.products_list, name='products_list'),
    path('add_products/', views.add_products, name='add_products'),
    path('edit_product/<pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<pk>/', views.delete_product, name='delete_product'),

    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('add_category/', views.CategoryCreate.as_view(), name='add_category'),
    path('edit_category/<pk>/', views.CategoryUpdate.as_view(), name='edit_category'),
    path('delete_category/<pk>/', views.CategoryDelete.as_view(), name='delete_category'),

    path('size_list/', views.add_size, name='size_list'),
    path('size_delete/<pk>/', views.SizeDelete.as_view(), name='size_delete'),

    path('color_list/', views.color_list, name='color_list'),
    path('color_delete/<pk>/', views.ColorDelete.as_view(), name='color_delete'),

    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit_stock/<pk>/',views.edit_stock, name='edit_stock'),
    path('stock_list/',views.stock_list, name='stock_list'),
    path('stock_delete/<pk>/', views.stock_delete, name='stock_delete'),

    path('order_list/', views.order_list, name='order_list'),
    path('order_status/<int:order_id>/', views.order_status_update, name="order_status_update"),

    path('coupon_list/', views.coupon_list, name='coupon_list'),
    path('add_coupon/',views.add_coupon, name='add_coupon'),
    path('edit_coupon/<pk>/', views.edit_coupon, name='edit_coupon'),
    path('coupon_delete/<pk>/', views.coupon_delete, name='coupon_delete'),

    path('banner_list/', views.banner_list, name='banner_list'),
    path('add_banner/',views.add_banner, name='add_banner'),
    path('edit_banner/<pk>/', views.edit_banner, name='edit_banner'),
    path('banner_delete/<pk>/', views.banner_delete, name='banner_delete'),
]
