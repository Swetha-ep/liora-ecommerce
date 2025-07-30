from django.shortcuts import render
from products.models import Inventory

# Create your views here.

def buy_now(request):
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
        }

    return render(request, 'checkout.html', context)