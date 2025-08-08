from django.db import models
from django.contrib.auth.models import User
from products.models import Inventory
from accounts.models import Address
# Create your models here.

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('RZP', 'Razorpay'),
    )
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_CHOICES)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid  = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)