from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('buy_now/', views.buy_now, name='buy_now'),
    path('place_order/',views.place_order,name='place_order'),

    path('verify_payment/<int:order_id>/',views.verify_payment, name='verify_payment'),
    path('orders/pay/<int:order_id>/',views.pay,name='razorpay_payment'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart_place_order/', views.cart_place_order, name='cart_place_order'),

    path('apply-coupon/', views.apply_coupon_ajax, name='apply_coupon_ajax'),
    path('apply-coupon-buy-now/', views.apply_coupon_buy_now_ajax, name='apply_coupon_buy_now_ajax'),

    path('your_orders/',views.your_orders, name='your_orders'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
