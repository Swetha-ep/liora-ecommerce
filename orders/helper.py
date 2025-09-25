from .models import Coupon
from django.utils import timezone

def send_order_email(order, user):
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.conf import settings

    subject = "Liora - Order Confirmation"
    html_message = render_to_string("email/order_confirm.html", {
        "user": user,
        "order": order,
    })

    email = EmailMessage(subject, html_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.content_subtype = "html"
    email.send()



def apply_coupon(user, cart_total, coupon_code):
    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True)
    except Coupon.DoesNotExist:
        raise ValueError("Invalid coupon code")
    
    now = timezone.now()
    if not (coupon.valid_from <= now <= coupon.valid_to):
        raise ValueError("This coupon is expired or not yet active")
    
    if coupon.users_used.filter(id=user.id).exists():
        raise ValueError("You have already used this coupon")
    
    if cart_total < coupon.min_order_amount:
        raise ValueError(f"Minimum order amount to use this coupon is ₹{coupon.min_order_amount}")
    
    discount = min(coupon.discount_amount, cart_total)
    final_total = cart_total - discount

    return final_total, discount, coupon
