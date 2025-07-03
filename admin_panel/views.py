from django.shortcuts import render
from products.models import Product,Categories

# Create your views here.
# dashboard view
def dashboard(request):
    return render(request, 'admin/dashboard.html')

# --------------------------product views-----------------------------

# product listing view
def products_list(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'items/products_list.html', context)

# add product view
def add_products(request):
    return render(request,'items/add_products.html')


# --------------------------category views-----------------------------

# category listing view
def category_list(request):
    categories = Categories.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'items/category_list.html', context)

# add category view
def add_category(request):
    return render(request,'items/add_category.html')