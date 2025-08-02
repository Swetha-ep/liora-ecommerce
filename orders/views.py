from django.shortcuts import render
from products.models import Inventory
from accounts.models import Address
from accounts.forms import AddressForm

# Create your views here.

def buy_now(request):
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm
    if request.method == 'POST':
        product = request.POST.get('product_id')
        size = request.POST.get('size_id')
        color = request.POST.get('color_id')
        quantity = request.POST.get('quantity')

        inventory = Inventory.objects.get(product=product,size=size,color=color)
        print(inventory)
        if not inventory or inventory.stock < int(quantity):
            message = "Stock unavailable"
        
        context = {
            'inventory' : inventory,
            'quantity' : quantity,
            'addresses' : addresses,
            'form' : form
        }

    return render(request, 'checkout.html', context)