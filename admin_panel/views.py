from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product, Categories, Size, Color, Inventory, Offer
from orders.models import Order, Coupon, OrderItem
from .models import Banner
from .forms import CategoryForm, ProductForm, ColorForm, SizeForm, StockForm, CouponForm, BannerForm, OfferForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test
from functools import wraps

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth_login')
        if not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# dashboard view
@superuser_required
def dashboard(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()

    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    data = (
        Order.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )

    labels = [d['month'].strftime('%b %Y') for d in data]
    values = [d['order_count'] for d in data]

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'labels': labels,
        'values': values,
    }
    return render(request, 'admin/dashboard.html', context)


def sales_report_pdf(request):
    # 🧮 Summary
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # 📅 Monthly Data
    monthly_data = (
        Order.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'), sales=Sum('total_price'))
        .order_by('month')
    )

    # 🏆 Top Products
    top_products = (
        OrderItem.objects.values('inventory__product__name')
        .annotate(total_qty=Sum('quantity'), total_sales=Sum('price'))
        .order_by('-total_qty')[:5]
    )

    # 📄 PDF Setup
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{datetime.date.today()}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # 🧾 Title
    title = Paragraph("<b>Liora — Sales Report</b>", styles['Title'])
    subtitle = Paragraph(f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}", styles['Normal'])
    elements.extend([title, subtitle, Spacer(1, 12)])

    # 📊 Summary Table
    summary_data = [
        ['Total Users', 'Total Orders', 'Total Sales (₹)'],
        [str(total_users), str(total_orders), f"₹{total_sales}"],
    ]
    summary_table = Table(summary_data, colWidths=[150, 150, 150])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.extend([Paragraph("<b>Summary</b>", styles['Heading2']), summary_table, Spacer(1, 20)])

    # 📅 Monthly Sales Table
    monthly_table_data = [['Month', 'Orders', 'Sales (₹)']]
    for m in monthly_data:
        monthly_table_data.append([
            m['month'].strftime('%B %Y'),
            str(m['order_count']),
            f"₹{m['sales'] or 0}"
        ])
    monthly_table = Table(monthly_table_data, colWidths=[200, 100, 150])
    monthly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.extend([Paragraph("<b>Monthly Sales Breakdown</b>", styles['Heading2']), monthly_table, Spacer(1, 20)])

    # 🏆 Top Products Table
    product_table_data = [['Product Name', 'Quantity Sold', 'Total Sales (₹)']]
    for p in top_products:
        product_table_data.append([
            p['inventory__product__name'] or 'N/A',
            str(p['total_qty']),
            f"₹{p['total_sales'] or 0}"
        ])
    product_table = Table(product_table_data, colWidths=[200, 100, 150])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.extend([Paragraph("<b>Top 5 Best-Selling Products</b>", styles['Heading2']), product_table])

    # ✅ Build PDF
    doc.build(elements)
    return response

# --------------------------category views-----------------------------

#--->- Class Based Views -<---

# category listing view
@method_decorator(superuser_required, name='dispatch')
class CategoryList(ListView):
    model = Categories
    template_name = 'items/category_list.html'
    context_object_name = 'categories'

# add category view
@method_decorator(superuser_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Categories
    success_url = reverse_lazy('category_list')
    template_name = 'items/add_category.html'
    form_class = CategoryForm

# edit category view
@method_decorator(superuser_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Categories
    success_url = reverse_lazy('category_list')
    template_name = 'items/add_category.html'
    form_class = CategoryForm

# delete category view
@method_decorator(superuser_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Categories
    context_object_name = 'category'
    success_url =reverse_lazy('category_list')


# --------------------------product views-----------------------------

# product listing view
@superuser_required
def products_list(request):
    products = Product.objects.all()

    page_number = request.GET.get('page',1)
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'products' : products,
        'page_obj' : page_obj,
    }
    return render(request, 'items/products_list.html', context)

# add product view
@superuser_required
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
@superuser_required
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
@superuser_required
def delete_product(request, pk):
    product = get_object_or_404(Product,id=pk)
    product.delete()
    return redirect('products_list')


# --------------------------size views-----------------------------
# size listing and adding view 
@superuser_required
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
@method_decorator(superuser_required, name='dispatch')
class SizeDelete(DeleteView):
    model = Size
    success_url =reverse_lazy('size_list')


# --------------------------color views-----------------------------
# color listing and adding view
@superuser_required
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
@method_decorator(superuser_required, name='dispatch')
class ColorDelete(DeleteView):
    model = Color
    success_url =reverse_lazy('color_list')


# --------------------------inventory views-----------------------------
#  add stock view
@superuser_required
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
@superuser_required
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
@superuser_required
def stock_list(request):
    stock = Inventory.objects.all()
    category = Categories.objects.all()

    category_id = request.GET.get('category')
    selected_category = None

    if category_id:
        stock = stock.filter(product__category_id=category_id)
        selected_category = Categories.objects.filter(id=category_id).first()

    paginator = Paginator(stock, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items' : page_obj,
        'categories' : category,
        'selected_category' : selected_category,
        'page_obj' : page_obj,
    }
    return render(request, 'inventory/stock_list.html', context)


# stock delete view
@superuser_required
def stock_delete(request, pk):
    stock = get_object_or_404(Inventory, id=pk)
    stock.delete()
    return redirect('stock_list')


# --------------------------order views-----------------------------
#order list
@superuser_required
def order_list(request):
    order = Order.objects.all().order_by('-created_at')
    return render(request, 'order/order_list.html', {'order': order})


# order status update
@superuser_required
def order_status_update(request, order_id):
    order = get_object_or_404(Order,id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status == 'Cancelled':
            messages.warning(request, "You cannot manually cancel an order from the admin panel.")
            return redirect(request.META.get("HTTP_REFERER", "order_list"))
        order.order_status = new_status
        order.save()
        messages.success(request, f"Order status updated to {new_status}.")
    return redirect(request.META.get("HTTP_REFERER", "order_list"))


# --------------------------coupon views-----------------------------
# coupon list
@superuser_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupon/coupon_list.html', {'coupons' : coupons})


# add coupon
@superuser_required
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
@superuser_required
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
@superuser_required
def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    coupon.delete()
    return redirect('coupon_list')


# --------------------------banner views-----------------------------
# add banner
@superuser_required
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
@superuser_required
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
@superuser_required
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'banner/banner_list.html',{'banners':banners})


# delete banner
@superuser_required
def banner_delete(request,pk):
    banner = get_object_or_404(Banner, id=pk)
    banner.delete()
    return redirect('banner_list')


# --------------------------offer views-----------------------------

#--->- Class Based Views -<---

# offer list
@method_decorator(superuser_required, name='dispatch')
class OfferList(ListView):
    model = Offer
    template_name = 'offer/offer_list.html'
    context_object_name = 'offers'


# add offer
@method_decorator(superuser_required, name='dispatch')
class OfferCreate(CreateView):
    model = Offer
    success_url = reverse_lazy('offer_list')
    template_name = 'offer/add_offer.html'
    form_class = OfferForm


# edit offer
@method_decorator(superuser_required, name='dispatch')
class OfferUpdate(UpdateView):
    model = Offer
    success_url = reverse_lazy('offer_list')
    template_name = 'offer/add_offer.html'
    form_class = OfferForm


# delete offer
@method_decorator(superuser_required, name='dispatch')
class OfferDelete(DeleteView):
    model = Offer
    context_object_name = 'offer'
    success_url = reverse_lazy('offer_list')