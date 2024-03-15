from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from django.contrib import messages
from django.http import HttpResponse
from .models import ProspectInfo
from django.db.models import Q
from tabernacle_customer_success import constants
class ProspectsListView(ListView):
    template_name = 'prospect/list_view.html'
    title = 'Prospect List'
    active_tab = 'prospect'
    model = ProspectInfo
    context_object_name = 'prospects'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            print("a")
            queryset = queryset.filter(
                (
                    Q(name__istartswith=search_query)
                    | Q(name__icontains=" " + search_query)
                )
            )
        return queryset.order_by("name")

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get("page_limit", constants.PAGINATION_LIMIT)
        if page_limit == "all":
            page_limit = len(queryset)
        return self.request.GET.get("paginate_by", page_limit)

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
        poc_info_form = prospectForms.PointOfContactForm(request.POST)
        print(prospect_info_form.errors)
        try:
            if prospect_info_form.is_valid() and poc_info_form.is_valid():
                prospect_info = prospect_info_form.save()
                point_of_contact_info = poc_info_form.save(commit=False)
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
            'poc_info_form': poc_info_form
        }
        return render(request, self.template_name, context)
