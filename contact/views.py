from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView


class ContactListView(ListView):
    template_name = 'contact/list_view.html'
    title = 'Contact Directory'
    active_tab = 'contact'

    def get(self, request, *args, **kwargs):
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        return render(request, self.template_name, context)



class ContactCreateView(View):
    template_name = 'contact/create_view.html'
    title = 'New Contact'
    active_tab = 'contact'

    def get(self, request, *args, **kwargs):
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        return render(request, self.template_name, context)
