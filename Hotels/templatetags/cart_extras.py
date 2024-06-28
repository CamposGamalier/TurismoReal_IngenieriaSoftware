# Hotels/templatetags/cart_extras.py
from django import template

register = template.Library()

@register.filter
def sum_total_price(cart_items):
    return sum(item.total_price for item in cart_items)
