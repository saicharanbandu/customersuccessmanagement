from django.contrib import messages
from django.shortcuts import render

from . import models as customerModels

def get_customer_info(request, customer_id):
    template = 'customer/customer_info.html'
    customer_profile = customerModels.Profile.objects.get(uuid=customer_id)
    context = {
        'customer_profile': customer_profile,
    }
    return render(request, template, context)