from django.db import models
from decimal import Decimal
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    name = models.CharField( max_length=50,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    image = models.ImageField(upload_to='category_images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):  
        return self.name
    

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='inventory_color')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images',blank=True,null=True)

    class Meta:
        unique_together = ('product','color','size')
    
    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','inventory')

    def __str__(self):
        return f'{self.user.username} - {self.inventory.product.name}'
    

class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='offer_images',blank=False, null=False)
    discount_type = models.CharField(
        max_length=10,
        choices=[("flat","Flat"),("percent","Percentage")],
        default="flat"
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def calculate_discount(self, total_amount):
        """Returns discounted amount based on this offer"""
        total = Decimal(total_amount)

        if self.discount_type == "flat":
            return Decimal(self.discount_value)
        elif self.discount_type == "percent":
            percent = Decimal(self.discount_value) / Decimal('100')
            return (total * percent).quantize(Decimal('0.01'))
        return Decimal('0.00')