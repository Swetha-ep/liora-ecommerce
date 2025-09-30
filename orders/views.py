from decimal import Decimal
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Inventory
from accounts.models import Address
from accounts.forms import AddressForm
from django.contrib import messages
from .models import Order, Cart, CartItem, OrderItem
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .helpers import send_order_email, apply_coupon


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
    

def apply_coupon_buy_now_ajax(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'message': 'Invalid request.'})

    subtotal = request.POST.get('subtotal')
    coupon_code = request.POST.get('coupon_code', '').strip()

    if not subtotal:
        return JsonResponse({'success': False, 'message': 'Subtotal not provided.'})

    try:
        subtotal = Decimal(subtotal)
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid subtotal.'})

    if not coupon_code:
        return JsonResponse({'success': False, 'message': 'Please enter a coupon code.'})

    try:
        final_total, discount, coupon = apply_coupon(request.user, subtotal, coupon_code)
        return JsonResponse({
            'success': True,
            'discount': float(discount),
            'final_total': float(final_total),
            'message': f'Coupon applied! You saved ₹{discount}'
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'message': str(e)})
    

def place_order(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        address_id = request.POST.get('address_id')
        quantity = int(request.POST.get('quantity'))
        total_price_submitted = Decimal(request.POST.get('total_price'))
        coupon_code = request.POST.get('coupon_code', "").strip()

        try:
            inventory = Inventory.objects.get(id=inventory_id)
            address = Address.objects.get(id=address_id)
            quantity = int(quantity)
            total_price_submitted = Decimal(total_price_submitted).quantize(Decimal('0.01'))
        except (Inventory.DoesNotExist, Address.DoesNotExist,ValueError, Decimal.InvalidOperation):
            messages.error(request, "Invalid input.")
            return redirect('buy_now')

        subtotal = inventory.product.price * quantity
       
        if coupon_code:
            try:
                final_total, discount, coupon = apply_coupon(request.user, subtotal, coupon_code)
                coupon.users_used.add(request.user)
                messages.success(request, f'Coupon applied! You saved ₹{discount}')
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('buy_now')
        else:
            final_total = subtotal

        tax = Decimal(20)
        total_calculated = (final_total + tax).quantize(Decimal('0.01'))

        if total_price_submitted != total_calculated:
            messages.error(request, "Payment amount mismatch. Please try again.")
            return redirect('buy_now')
        
        order = Order.objects.create(
            user = request.user,
            address = address,
            total_price=total_calculated,
            is_paid = False,
            order_status = 'Pending',
            payment_method='COD',
        )

        OrderItem.objects.create(
            order=order,
            inventory=inventory,
            quantity=quantity,
            price=inventory.product.price * quantity,
        )

        inventory.stock -= quantity
        inventory.save()
 
        return redirect('razorpay_payment', order_id=order.id)
         
    messages.error(request, "Invalid request.")
    return redirect('index')  



@csrf_exempt
def verify_payment(request, order_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure'}, status=400)

        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.is_paid = True
        order.payment_method = 'RZP'
        order.save()

        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_items.delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid'}, status=400)

    

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
            send_order_email(order, order.user)

            context = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': int(order.total_price * 100),
                'auto_open_razorpay': True  
            }
            return render(request, 'orders/payment.html', context)

        elif payment_method == 'COD':
            order.payment_method = 'COD'
            order.is_paid = False
            order.save()
            send_order_email(order, order.user)

            cart_items = CartItem.objects.filter(cart__user=request.user)
            cart_items.delete()
            
            messages.success(request, "Order placed with Cash on Delivery.")
            return redirect('your_orders')

    return render(request, 'orders/payment.html', {'order': order, 'auto_open_razorpay': False})



def your_orders(request):
    order = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders' : order,
    }
    return render(request, 'orders/your_orders.html', context)


@login_required
def add_to_cart(request):
    if request.method=='POST':
        product = request.POST.get('product_id')
        size = request.POST.get('size_id')
        color = request.POST.get('color_id')
        quantity = int(request.POST.get('quantity', 1))
    
    try:
        inventory = Inventory.objects.get(product=product, size=size, color=color)
    except Inventory.DoesNotExist:
        messages.error(request, "Invalid product selection.")
        return redirect('index')

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, inventory=inventory)

    if item_created:
            if quantity > inventory.stock:
                messages.error(request, "Stock unavailable.")
                return redirect('product_detail', pk=product)
            item.quantity = quantity
    else:
        if item.quantity + quantity > inventory.stock:
            messages.error(request, "Stock unavailable.")
            return redirect('product_detail', pk=product)
        item.quantity += quantity

    item.save()
    messages.success(request, "Item added to cart. ")
    return redirect('cart')


def cart(request):
    addresses = Address.objects.filter(user=request.user)
    cart = (Cart.objects.filter(user=request.user).prefetch_related('items__inventory__product').first())
    context = {
        'cart' : cart,
        'addresses' : addresses,
    }
    return render(request, 'orders/cart.html', context)


def update_cart_quantity(request, item_id):
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)

            cart_item.quantity = quantity
            cart_item.save()

            row_total = cart_item.quantity * cart_item.inventory.product.price
            cart_total = sum(
                i.quantity * i.inventory.product.price for i in cart_item.cart.items.all()
            )

            tax = 20
            grand_total = cart_total + tax

            return JsonResponse({
                "success": True,
                "row_total": row_total,
                "cart_total": cart_total,
                "tax": str(tax),
                "grand_total": str(grand_total),
            })

        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


def cart_place_order(request):
    if request.method =='POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('cart')
        
        address_id = request.POST.get('selected_address')
        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect("cart")

        address = get_object_or_404(Address, id=address_id, user=request.user)

        total_calculated = sum(item.inventory.product.price * item.quantity for item in cart_items)
        tax = 20
        final_total = total_calculated + tax
        discount = 0
        
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            try:
                final_total, discount, coupon = apply_coupon(request.user, final_total, coupon_code)
                coupon.users_used.add(request.user)
                messages.success(request, f'Coupon applied! You saved ₹{discount}')
            except ValueError as e:
                messages.error(request, str(e))
                final_total = total_calculated + tax

        order = Order.objects.create(
            user = request.user,
            address = address,
            total_price=final_total,
            is_paid = False,
            order_status = 'Pending',
            payment_method = 'COD',
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                inventory=item.inventory,
                quantity=item.quantity,
                price=item.inventory.product.price * item.quantity 
            )

            item.inventory.stock -= item.quantity
            item.inventory.save()

        return redirect('razorpay_payment', order_id=order.id)
    return redirect('cart')
 

def apply_coupon_ajax(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.inventory.product.price * item.quantity for item in cart_items) + 20
    coupon_code = request.POST.get('coupon_code', '').strip()

    if not coupon_code:
        return JsonResponse({'success' : False, 'message':'Please enter a coupon code.'})
    
    try:
        final_total, discount, coupon = apply_coupon(request.user, cart_total, coupon_code)
        return JsonResponse({
            'success' : True,
            'discount' : float(discount),
            'final_total' : float(final_total),
            'message' : f'Coupon applied! You saved ₹{discount}'
        })
    except ValueError as e:
        return JsonResponse({'success' : False, 'message': str(e)})