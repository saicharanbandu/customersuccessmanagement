
from django import template
  
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