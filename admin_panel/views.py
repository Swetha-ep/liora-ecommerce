from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product, Categories, Size, Color, Inventory
from orders.models import Order, Coupon
from .models import Banner
from .forms import CategoryForm, ProductForm, ColorForm, SizeForm, StockForm, CouponForm, BannerForm
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


# --------------------------order views-----------------------------
#order list
def order_list(request):
    order = Order.objects.all().order_by('-created_at')
    return render(request, 'order/order_list.html', {'order': order})


# order status update
def order_status_update(request, order_id):
    order = get_object_or_404(Order,id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        order.order_status = new_status
        order.save()
    return redirect(request.META.get("HTTP_REFERER", "order_list"))


# --------------------------coupon views-----------------------------
# coupon list
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupon/coupon_list.html', {'coupons' : coupons})


# add coupon
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm()
    return render(request, 'coupon/add_coupon.html', {'form' : form})


# edit coupon
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'coupon/add_coupon.html',{'form':form})


# delete coupon
def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    coupon.delete()
    return redirect('coupon_list')


# --------------------------banner views-----------------------------
# add banner
def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('banner_list')
    else:
        form = BannerForm()
    return render(request, 'banner/add_banner.html',{'form':form})


# edit banner
def edit_banner(request,pk):
    banner = get_object_or_404(Banner, id=pk)
    if request.method=='POST':
        form = BannerForm(request.POST,request.FILES,instance=banner)
        if form.is_valid():
            form.save()
            return redirect('banner_list')
    else:
        form=BannerForm(instance=banner)
    return render(request, 'banner/add_banner.html', {'form':form})


# banner list
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'banner/banner_list.html',{'banners':banners})


# delete banner
def banner_delete(request,pk):
    banner = get_object_or_404(Banner, id=pk)
    banner.delete()
    return redirect('banner_list')