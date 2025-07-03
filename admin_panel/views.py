from django.shortcuts import render
from products.models import Product

# Create your views here.
def dashboard(request):
    return render(request, 'admin/dashboard.html')

def products_list(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'items/products_list.html', context)