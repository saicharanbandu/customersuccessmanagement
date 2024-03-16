# Dango Imports
from django.shortcuts import render

from misc import models as miscModels

def load_states(request):
    country_id = request.GET.get('country_id')
    states = miscModels.State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'misc/state_dropdown_list.html', {'states': states})