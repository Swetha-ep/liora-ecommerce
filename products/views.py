from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from admin_panel.models import Banner
from .helper import get_product_offer_details
from django.contrib import messages
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required


# home page view
def index(request):
    banners = Banner.objects.filter(is_active=True)
    offers = Offer.objects.filter(active=True)
    all_products = list(Product.objects.all())
    best_sellers = random.sample(all_products, min(len(all_products), 4))

    context = {
        'banners' : banners,
        'offers' : offers,
        'best_sellers': best_sellers,
    }
    return render(request,'index.html',context)


# category page view
def shop(request):
    categories = Categories.objects.all()
    return render(request,'shop.html',{'categories' : categories})


# ------------------------------------------product views----------------------------------
# products page view
def products(request, slug=None):
    category = None
    if slug == 'all' or slug is None:
        category = None
        category_name = "All Products"
        items = Product.objects.all().order_by('-id')
    else:
        category = get_object_or_404(Categories, slug=slug)
        category_name = category.name
        items = Product.objects.filter(category=category).order_by('-id')

    search_query = request.GET.get('q')
    if search_query:
        items = items.filter(name__icontains=search_query)

    sort_option = request.GET.get('sort')

    if sort_option == 'low':
        items = items.order_by('price')
    elif sort_option == 'high':
        items = items.order_by('-price')

    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    offers = Offer.objects.filter(category=category, active=True)
    offer = offers.first()

    for item in page_obj:
        offer_data = get_product_offer_details(item)
        item.discounted_price = offer_data['discounted_price']
        item.offer = offer_data['offer']

    categories = Categories.objects.all()
    
    context = {
        'items' : page_obj,
        'category_name' : category_name,
        'categories' : categories,
        'offer': offer,
        'page_obj' : page_obj,
        'category': category,
    }
    return render(request,'products.html', context)

# product detail view
def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    colors = Color.objects.filter(inventory_color__product = product).distinct()

    offer = Offer.objects.filter(category=product.category, active=True).first()

    offer_data = get_product_offer_details(product)
    discounted_price = offer_data['discounted_price']
    offer = offer_data['offer']
    savings = offer_data['savings']

    all_products = list(Product.objects.filter(category=product.category))
    best_sellers = random.sample(all_products, min(len(all_products), 4))

    selected_color_id = request.GET.get('color')
    inventory = None
    if selected_color_id:
        selected_color = get_object_or_404(Color, id=selected_color_id)
        inventory = Inventory.objects.filter(product=product, color_id=selected_color_id).first()
    else:
        selected_color = colors.first()

    wishlisted = False
    if request.user.is_authenticated and inventory:
        wishlisted = Wishlist.objects.filter(user=request.user, inventory=inventory).exists()
    

    inventories = Inventory.objects.filter(
        product=product, 
        color=selected_color,
        stock__gt=0)

    context = {
        'product' : product,
        'colors' : colors,
        'selected_color' : selected_color,
        'inventories' : inventories,
        'discounted_price': discounted_price,
        'offer': offer,
        'savings' : savings,
        'wishlisted': wishlisted,
        'best_sellers' : best_sellers,
    }
    return render(request, 'products/product_details.html', context)

# -----------------------------------------end of product views----------------------------

# ----------------------------------------wishlist views----------------------------------
# add to wishlist view 
@login_required(login_url='auth_login')
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        color_id = request.POST.get('color_id')

        inventory = Inventory.objects.filter(
            product_id=product_id,
            color_id=color_id
        ).first()

        if not inventory:
            messages.error(request, 'Selected color is not available.')
            return redirect('product_view', slug=inventory.product.slug)
    

        item, created = Wishlist.objects.get_or_create(
            user=request.user, 
            inventory=inventory
            )
        
        if created:
            messages.success(request, "Product added to your wishlist")
        else:
            messages.info(request, "Product is already in your wishlist")

        return redirect('product_view', slug=inventory.product.slug)


# wishlist view
@login_required(login_url='auth_login')
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('inventory')
    for item in items:
        offer = Offer.objects.filter(category=item.inventory.product.category, active=True).first()
        offer_data = get_product_offer_details(item.inventory.product)
        item.discounted_price = offer_data['discounted_price']
        item.offer = offer_data['offer']
        item.savings = offer_data['savings']
    context = {
        'items' : items,
    }
    return render(request, 'products/wishlist.html',context)


# remove from wishlist view
@login_required(login_url='auth_login')
def wishlist_remove(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    Wishlist.objects.filter(user=request.user, inventory=inventory).delete()
    messages.success(request, 'Product removed from your wishlist')
    return redirect('wishlist')

# ---------------------------------------end of wishlist views--------------------------

# blog view
def blog(request):
    return render(request, 'blog.html')


# contact view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            subject = f"New Message from {name} via Liora Contact Form"
            full_message = f'Message from {name} ({email}):\n\n{message}'

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,  
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully 💌")
                return redirect('contact')
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
                return redirect('contact')

    else:
        form = ContactForm()
    return render(request, 'contact.html',{'form': form})