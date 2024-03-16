from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from django.http import HttpResponse
from tabernacle_customer_success import constants

class ProspectsListView(ListView):
    template_name = 'prospect/list_view.html'
    title = 'Prospect List'
    active_tab = 'prospect'
    model = prospectModels.Profile
    context_object_name = 'prospects'


    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)
    
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
        prospect_form = prospectForms.ProspectInfoForm()
        poc_form = prospectForms.PointOfContactForm()
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_form': poc_form

        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectInfoForm(request.POST)
        poc_form = prospectForms.PointOfContactForm(request.POST)
        print(prospect_form.errors)
        print(poc_form.errors)

        try:
            if prospect_form.is_valid() and poc_form.is_valid():
                prospect_object = prospect_form.save()
                point_of_contact_info = poc_form.save(commit=False)
                point_of_contact_info.prospect = prospect_object
                point_of_contact_info.save()
                return redirect('prospect:list')
        except Exception as e:
            error_message = f'An error occurred: {e}'
            return HttpResponse(error_message, status=500)
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_form': poc_form
        }
        return render(request, self.template_name, context)
