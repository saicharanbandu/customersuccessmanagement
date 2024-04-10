
from django import template
from decimal import Decimal, ROUND_HALF_UP
  
register = template.Library()
  
@register.filter()
def plan_name(value):
    return value.split('_')[0]

@register.filter()
def plan_amount(value):
    return value.split('_')[1]

@register.filter()
def plan_size(value):
    return f'{value.split('_')[3]}'

@register.filter()
def plan_discount_15(value):
    value = Decimal(value)
    discount_percentage = 15

    discount_percentage_decimal = Decimal(discount_percentage)
    discount_amount = (discount_percentage_decimal / Decimal(100)) * value
    discounted_price = value - discount_amount
    rounded_discounted_price = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return rounded_discounted_price

@register.filter()
def plan_discount_20(value):
    value = Decimal(value)
    discount_percentage = 20

    discount_percentage_decimal = Decimal(discount_percentage)
    discount_amount = (discount_percentage_decimal / Decimal(100)) * value
    discounted_price = value - discount_amount
    rounded_discounted_price = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return rounded_discounted_price
