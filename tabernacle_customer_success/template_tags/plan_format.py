
from django import template
from tabernacle_customer_success import helper

register = template.Library()
  
@register.filter()
def plan_name(value):
    return value.split('_')[0]

@register.filter()
def plan_amount(value):
    return value.split('_')[1]

@register.filter()
def plan_size(value):
    return value.split('_')[3]

@register.filter()
def plan_discount_15(value):
    discounted_amount = helper.get_discounted_amount(value, 15)
    return discounted_amount

@register.filter()
def plan_discount_20(value):
    discounted_amount = helper.get_discounted_amount(value, 20)
    return discounted_amount
