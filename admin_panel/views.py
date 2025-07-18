from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product, Categories, Size, Color, Inventory
from .forms import CategoryForm, ProductForm, ColorForm, SizeForm, StockForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# dashboard view
def dashboard(request):
    return render(request, 'admin/dashboard.html')



# --------------------------category views-----------------------------

#--->- Class Based Views -<---

# category listing view
class CategoryList(ListView):
    model = Categories
    template_name = 'items/category_list.html'
    context_object_name = 'categories'

# add category view
class CategoryCreate(CreateView):
    model = Categories
    success_url = reverse_lazy('category_list')
    template_name = 'items/add_category.html'
    form_class = CategoryForm

# edit category view
class CategoryUpdate(UpdateView):
    model = Categories
    success_url = reverse_lazy('category_list')
    template_name = 'items/add_category.html'
    form_class = CategoryForm

# delete category view
class CategoryDelete(DeleteView):
    model = Categories
    context_object_name = 'category'
    success_url =reverse_lazy('category_list')


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
    heading = "Add Product"
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()
    return render(request,'items/add_category.html',
                  {'form':form, 'heading': heading})

# edit product view
def edit_product(request, pk):
    heading = "Edit Product"
    product = get_object_or_404(Product, id = pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    return render(request,'items/add_category.html',
                  {'form':form, 'heading': heading})

# delete product view
def delete_product(request, pk):
    product = get_object_or_404(Product,id=pk)
    product.delete()
    return redirect('products_list')


# --------------------------size views-----------------------------
# size listing and adding view 
def add_size(request):
    sizes = Size.objects.all()
    form = SizeForm()

    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('size_list')
    
    context = {
        'delete_url_name' : 'size_delete',
        'heading' : 'Size',
        'property' : sizes,
        'form' :form
    }
    return render(request, 'inventory/property_list.html', context)

# size delete view
class SizeDelete(DeleteView):
    model = Size
    success_url =reverse_lazy('size_list')


# --------------------------color views-----------------------------
# color listing and adding view
def color_list(request):
    colors = Color.objects.all()
    form = ColorForm()
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('color_list')
    context = {
        'delete_url_name' : 'color_delete',
        'heading' : 'Color',
        'property' : colors,
        'form' : form,
    }
    return render(request,'inventory/property_list.html',context)


# color delete view
class ColorDelete(DeleteView):
    model = Color
    success_url =reverse_lazy('color_list')


# --------------------------inventory views-----------------------------
#  add stock view
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'inventory/add_stock.html',{'form' : form})


# edit stock view
def edit_stock(request, pk):
    heading = 'Edit Stock'
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == 'POST':
        form = StockForm(request.POST,request.FILES,instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm(instance=inventory)
    return render(request, 
                  'inventory/add_stock.html', 
                  {'form' : form, 'heading' : heading})


# stock list view
def stock_list(request):
    stock = Inventory.objects.all()
    category = Categories.objects.all()

    category_id = request.GET.get('category')
    selected_category = None

    if category_id:
        stock = stock.filter(product__category_id=category_id)
        selected_category = Categories.objects.filter(id=category_id).first()

    context = {
        'items' : stock,
        'categories' : category,
        'selected_category' : selected_category,
    }
    return render(request, 'inventory/stock_list.html', context)


# stock delete view
def stock_delete(request, pk):
    stock = get_object_or_404(Inventory, id=pk)
    stock.delete()
    return redirect('stock_list')

