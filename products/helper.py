from decimal import Decimal, ROUND_HALF_UP
from .models import Offer

def quantize(d):
    return d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def get_product_offer_details(product):
    """
    Returns a dict {'offer', 'discounted_price', 'savings'}.
    This version APPLIES the offer directly to the product price (no min-order check).
    """
    offer = Offer.objects.filter(category=product.category, active=True).first()
    original = Decimal(product.price)
    discounted_price = original
    savings = Decimal('0.00')

    if not offer:
        return {'offer': None, 'discounted_price': quantize(original), 'savings': savings}

    discount_value = Decimal(offer.discount_value)

    if offer.discount_type == 'percent':
        discount_percentage = discount_value / Decimal('100')
        discounted_price = original * (Decimal('1') - discount_percentage)
    else:  # flat
        discounted_price = original - discount_value

    if discounted_price < 0:
        discounted_price = Decimal('0.00')

    discounted_price = quantize(discounted_price)
    savings = quantize(original - discounted_price)

    return {
        'offer': offer,
        'discounted_price': discounted_price,
        'savings': savings
    }

