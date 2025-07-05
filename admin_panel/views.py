from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product,Categories
from .forms import CategoryForm

# Create your views here.
# dashboard view
def dashboard(request):
    return render(request, 'admin/dashboard.html')



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
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        form = CategoryForm()
    return render(request,'items/add_category.html',{'form':form})

# edit category view
def edit_category(request, pk):
    category = get_object_or_404(Categories, id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
        return redirect('category_list')
    form = CategoryForm(instance = category)
    return render(request, 'items/add_category.html',{'form':form})

# delete category view
def delete_category(request, pk):
    category = get_object_or_404(Categories, id=pk)
    category.delete()
    return redirect('category_list')


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
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()
    return render(request,'items/add_products.html',{'form':form})
