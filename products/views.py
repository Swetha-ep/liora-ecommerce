from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def products(request, slug=None):
    if slug:
        category = get_object_or_404(Categories, slug=slug)
        items = Product.objects.filter(category=category)
        category_name = category.name
    else:
        items = Product.objects.filter(category=category)
        category_name = "All Products"

    categories = Categories.objects.all()
    
    context = {
        'items' : items,
        'category_name' : category_name,
        'categories' : categories,
    }
    return render(request,'products.html', context)

def shop(request):
    categories = Categories.objects.all()
    return render(request,'shop.html',{'categories' : categories})


def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    inventory = Inventory.objects.filter(product=product)
    context = {
        'item' : inventory,
    }
    return render(request, 'products/product_details.html', context)