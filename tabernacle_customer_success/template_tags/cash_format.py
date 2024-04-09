
from django import template
  
register = template.Library()
  
@register.filter()
def inr(value):
    s, *d = str(value).partition(".")
    r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    if d[1] == '00':
        return "".join([r])
    else:
        return "".join([r] + d)