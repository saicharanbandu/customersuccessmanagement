from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models as customerModels



@login_required
def get_customer_info(request, customer_id):
    template = 'customer/_partials/_info_view.html'
    customer_profile = customerModels.Profile.objects.get(uuid=customer_id)
    context = {
        'customer': customer_profile,
    }
    return render(request, template, context)