from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('buy_now/', views.buy_now, name='buy_now'),
    path('place_order/',views.place_order,name='place_order'),
    path('orders/pay/<int:order_id>/',views.pay,name='razorpay_payment'),
    path('your_orders/',views.your_orders, name='your_orders'),
]
