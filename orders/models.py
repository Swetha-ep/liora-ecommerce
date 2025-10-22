from django.db import models
from django.contrib.auth.models import User
from products.models import Inventory
from accounts.models import Address
from django.conf import settings
from decimal import Decimal
from products.helper import get_product_offer_details
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
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_CHOICES)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid  = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'{self.inventory.product.name} - ({self.quantity})'
    
    @property
    def subtotal(self):
        offer_details = get_product_offer_details(self.inventory.product)
        discounted_price = offer_details['discounted_price']
        return discounted_price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.inventory.product.name} - {self.quantity}"
    
    @property
    def subtotal(self):
        offer_details = get_product_offer_details(self.inventory.product)
        discounted_price = offer_details['discounted_price']
        return discounted_price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    users_used = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.code
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s wallet"
    
    def deposit(self, amount, description=""):
        self.balance += Decimal(amount)
        self.save()
        WalletTransaction.objects.create(wallet=self, amount=amount, transaction_type='Credit', description=description)

    def withdraw(self, amount, description=""):
        if self.balance >= amount:
            self.balance -= Decimal(amount)
            self.save()
            WalletTransaction.objects.create(wallet=self, amount=amount, transaction_type='Debit', description=description)
        else:
            raise ValueError("Insufficient balance")

    
class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} ({self.wallet.user.username})'
    