import re
from django import template

register = template.Library()

@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        if field_name == 'page_limit' and 'page' in urlencode:
            if re.search("page=\d*", urlencode):
                urlencode = re.sub("page=\d*", "page=1", urlencode)
            if re.search("page=\d*&?", urlencode):
                urlencode = re.sub("page=\d*&?", "page=1&", urlencode)
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.filter
def attributes_exists(queryset, attribute):
    return any(getattr(query.profile, attribute) is not None for query in queryset)

