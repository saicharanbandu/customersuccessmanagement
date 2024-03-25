from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from django.http import HttpResponse
from tabernacle_customer_success import constants
from django.contrib import messages

from django.db.models import Q

class ProspectsListView(ListView):
    template_name = 'prospect/list_view.html'
    title = 'Prospect List'
    active_tab = 'prospect'
    model = prospectModels.Profile
    context_object_name = 'prospects'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                (
                    Q(name__istartswith=search_query)
                    | Q(name__icontains=" " + search_query)
                )
            )
        return queryset.order_by("name")

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        more_context = {
            "title": self.title,
            "active_tab": self.active_tab,
        }
        context.update(more_context)
        return context



class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(prefix='prospect')
        poc_form = prospectForms.PointOfContactForm(prefix='poc')
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_form': poc_form

        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(request.POST, prefix='prospect')
        poc_form = prospectForms.PointOfContactForm(request.POST, prefix='poc')

        try:
            if prospect_form.is_valid() and poc_form.is_valid():
                prospect_object = prospect_form.save()
                point_of_contact_info = poc_form.save(commit=False)
                point_of_contact_info.prospect = prospect_object
                point_of_contact_info.save()
                messages.success(request, 'Prospect has been successfully created')
                return redirect('prospect:list')
        except Exception as e:
            messages.error(request, 'Unsuccessful, try again')
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_form': poc_form
        }
        return render(request, self.template_name, context)
