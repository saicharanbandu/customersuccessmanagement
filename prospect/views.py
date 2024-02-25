from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView


class ProspectsListView(ListView):
    template_name = 'prospect/list_view.html'
    title = 'Prospect List'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        return render(request, self.template_name, context)



class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        return render(request, self.template_name, context)
