from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Inventory
from accounts.models import Address
from accounts.forms import AddressForm
from django.contrib import messages
from .models import Order
import razorpay
from django.conf import settings


# Create your views here.

def buy_now(request):
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        product = request.POST.get('product_id')
        size = request.POST.get('size_id')
        color = request.POST.get('color_id')
        quantity = request.POST.get('quantity')

        try:
            inventory = Inventory.objects.get(product=product, size=size, color=color)
            if inventory.stock < int(quantity):
                messages.error(request, "Stock unavailable.")
                return redirect('product_detail', pk=product)
            
        except Inventory.DoesNotExist:
            messages.error(request, "Invalid product selection.")
            return redirect('index')
        
        context = {
            'inventory' : inventory,
            'quantity' : quantity,
            'addresses' : addresses,
            
        }
        return render(request, 'checkout.html', context)

    else:
        messages.error(request, "Invalid access to checkout.")
        return redirect('index')
    

def place_order(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        address_id = request.POST.get('address_id')
        quantity = int(request.POST.get('quantity'))
        total_price_submitted = Decimal(request.POST.get('total_price'))

        try:
            inventory = Inventory.objects.get(id=inventory_id)
            address = Address.objects.get(id=address_id)
            quantity = int(quantity)
            total_price_submitted = Decimal(total_price_submitted).quantize(Decimal('0.01'))
        except (Inventory.DoesNotExist, Address.DoesNotExist,ValueError, Decimal.InvalidOperation):
            messages.error(request, "Invalid input.")
            return redirect('buy_now')

        subtotal = inventory.product.price * quantity
        tax = Decimal(20)
        total_calculated = (subtotal + tax).quantize(Decimal('0.01'))

        if total_price_submitted != total_calculated:
            messages.error(request, "Payment amount mismatch. Please try again.")
            return redirect('buy_now')
        
        order = Order.objects.create(
            user = request.user,
            inventory = inventory,
            address = address,
            quantity = quantity,
            total_price = total_calculated,
            is_paid = False,
            order_status = 'Pending',
            payment_method='COD',
        )
        

        return redirect('razorpay_payment', order_id=order.id)
         
    messages.error(request, "Invalid request.")
    return redirect('index')  


def pay(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'RZP':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(dict(
                amount=int(order.total_price * 100),
                currency='INR',
                payment_capture='1'
            ))
            order.payment_method = 'RZP'
            order.razorpay_order_id = razorpay_order['id']
            order.save()

            # Render Razorpay payment page with keys
            context = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': int(order.total_price * 100),
            }
            return render(request, 'orders/payment.html', context)

        elif payment_method == 'COD':
            order.payment_method = 'COD'
            order.is_paid = False
            order.save()
            messages.success(request, "Order placed with Cash on Delivery.")
            return redirect('your_orders')

    return render(request, 'orders/payment.html', {'order': order})


def your_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/your_orders.html',{'orders' : orders})
