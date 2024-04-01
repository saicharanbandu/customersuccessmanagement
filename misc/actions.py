# Dango Imports
from django.shortcuts import render

from misc import models as miscModels

def load_states(request):
    template = 'misc/state_dropdown_list.html'
    country_id = request.GET.get('country_id')
    states = miscModels.State.objects.filter(country_id=country_id).order_by('name')
    return render(request, template, {'states': states})