from django.db import models
from django.utils.text import slugify

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
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images',blank=True,null=True)

    class Meta:
        unique_together = ('product','color','size')
    
    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"