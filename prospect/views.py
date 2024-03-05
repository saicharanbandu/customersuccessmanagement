from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from django.contrib import messages
from django.http import HttpResponse
from .models import ProspectInfo

class ProspectsListView(ListView):
    template_name = 'prospect/list_view.html'
    title = 'Prospect List'
    active_tab = 'prospect'
    model = ProspectInfo
    context_object_name = 'prospects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        more_context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        context.update(more_context)
        return context



class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_info_form = prospectForms.ProspectInfoForm()
        pOC_info_form = prospectForms.PointOfContactForm()
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_info_form': prospect_info_form,
            'pOC_info_form': pOC_info_form

        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        prospect_info_form = prospectForms.ProspectInfoForm(request.POST)
        pOC_info_form = prospectForms.PointOfContactForm(request.POST)
        try:
            if prospect_info_form.is_valid() and pOC_info_form.is_valid():
                prospect_info = prospect_info_form.save()
                point_of_contact_info = pOC_info_form.save(commit=False)
                point_of_contact_info.prospect = prospect_info
                point_of_contact_info.save()
                print("Prospect and POC Data saved")
                return redirect('prospect:list')
        except Exception as e:
            error_message = f'An error occurred: {e}'
            return HttpResponse(error_message, status=500)
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_info_form': prospect_info_form,
            'pOC_info_form': pOC_info_form
        }
        return render(request, self.template_name, context)
