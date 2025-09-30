from django.shortcuts import render, get_object_or_404
from .models import *
from admin_panel.models import Banner

# Create your views here.
def index(request):
    banners = Banner.objects.filter(is_active=True)
    return render(request,'index.html',{'banners' : banners})

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
    colors = Color.objects.filter(inventory_color__product = product).distinct()

    selected_color_id = request.GET.get('color')
    if selected_color_id:
        selected_color = get_object_or_404(Color, id=selected_color_id)
    else:
        selected_color = colors.first()

    inventories = Inventory.objects.filter(
        product=product, 
        color=selected_color,
        stock__gt=0)

    context = {
        'product' : product,
        'colors' : colors,
        'selected_color' : selected_color,
        'inventories' : inventories,
    }
    return render(request, 'products/product_details.html', context)