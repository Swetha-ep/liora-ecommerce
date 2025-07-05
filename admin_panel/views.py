from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product,Categories
from .forms import CategoryForm
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
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()
    return render(request,'items/add_products.html',{'form':form})
