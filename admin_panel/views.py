from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product, Categories, Size, Color
from .forms import CategoryForm, ProductForm
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
class SizeList(ListView):
    model = Size
    template_name = 'inventory/property_list.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url_name'] = 'size_delete'
        context['heading'] = 'Size'
        return context

class SizeDelete(DeleteView):
    model = Size
    success_url =reverse_lazy('size_list')


# --------------------------color views-----------------------------
class ColorList(ListView):
    model = Color
    template_name = 'inventory/property_list.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url_name'] = 'color_delete'
        context['heading'] = 'Color'
        return context
    

class ColorDelete(DeleteView):
    model = Color
    success_url =reverse_lazy('color_list')


# --------------------------inventory views-----------------------------