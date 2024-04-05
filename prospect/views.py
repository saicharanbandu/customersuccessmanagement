from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from django.http import HttpResponse
from tabernacle_customer_success import constants
from django.contrib import messages
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

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
        PointOfContactFormSet = formset_factory(prospectForms.PointOfContactForm, extra=2)
        poc_formset = PointOfContactFormSet()
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(request.POST, prefix='prospect')
        PointOfContactFormSet = formset_factory(prospectForms.PointOfContactForm, extra=2)
        poc_formset = PointOfContactFormSet(request.POST)

        try:
            if prospect_form.is_valid() and poc_formset.is_valid():
                prospect_object = prospect_form.save()
                for form in poc_formset:
                    point_of_contact_info = form.save(commit=False)
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
            'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)

class ProspectEditView(View):
    template_name = 'prospect/edit_view.html'
    title = 'Edit Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(instance=prospect_instance, prefix='prospect')

        # # Retrieve existing point of contacts for the prospect
        # existing_pocs = prospect_instance.prospect_poc.all()
        # # Generate initial data for the point of contact formset
        # poc_initial = [{'name': poc.name, 'email': poc.email, 'mobile': poc.mobile, 'remarks': poc.remarks} for poc in existing_pocs]
        # # Create formset with initial data
        # PointOfContactFormSet = formset_factory(prospectForms.PointOfContactForm, extra=0)
        # poc_formset = PointOfContactFormSet(initial=poc_initial, prefix='poc')

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            # 'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(request.POST, instance=prospect_instance, prefix='prospect')
        
        
        # poc_formset = prospectForms.PointOfContactFormSet(request.POST, prefix='poc')

        try:
            if prospect_form.is_valid() :
                prospect_form.save()
                

                messages.success(request, 'Prospect information has been successfully updated')
                return redirect('prospect:list')
            else:
                # Print form errors for debugging
                print(prospect_form.errors)
                
                messages.error(request, 'Unsuccessful, try again')
        except Exception as e:
            # Print the exception for debugging
            print(e)
            messages.error(request, 'Unsuccessful, try again')

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            # 'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)



PointOfContactFormSet = modelformset_factory(prospectModels.PointOfContact, form=prospectForms.PointOfContactForm, extra=0, exclude=())   
class UpdatePointOfContactView(View):
    model = prospectModels.PointOfContact
    form_class = prospectForms.PointOfContactForm
    template_name = 'prospect/update_poc.html'

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        
        prospect_formset = PointOfContactFormSet(queryset=prospect_instance.prospect_poc.all(), prefix='form')

        context = {
        'title': 'Edit Point of Contact',
        'prospect_formset': prospect_formset,
        'prospect_instance': prospect_instance,
        'active_tab': 'prospect',
    }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        print(request.POST)
        prospect_formset =PointOfContactFormSet(request.POST, queryset=prospect_instance.prospect_poc.all(), prefix='form')
        print(prospect_formset)
        print(request.POST)
        queryset=prospect_instance.prospect_poc.all()
        print(queryset)
        if prospect_formset.is_valid():
            print('valid')
            prospect_formset.save()
            messages.success(request, 'Point of Contact updated successfully')
            return redirect('prospect:view', ob=prospect_instance.slug)
        else:
            print(prospect_formset.errors)
            prospect_formset = PointOfContactFormSet(queryset=prospect_instance.prospect_poc.all(), prefix='form')
            messages.error(request, 'Unable to update Point of Contact. Try again.')

        context = {
            'title': 'Edit Point of Contact',
            'prospect_formset': prospect_formset,
            'prospect_instance': prospect_instance,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)
    
    
    
    
class UpdatePointOfContactView(View):
    template_name = 'prospect/update_poc.html'

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_formset = PointOfContactFormSet(queryset=prospect_instance.prospect_poc.all(), prefix='form')

        context = {
            'title': 'Edit Point of Contact',
            'prospect_formset': prospect_formset,
            'prospect_instance': prospect_instance,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = request.POST.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_formset = PointOfContactFormSet(request.POST, queryset=prospect_instance.prospect_poc.all(), prefix='form')

        if prospect_formset.is_valid():
            prospect_formset.save()
            messages.success(request, 'Point of Contact updated successfully')
            return redirect('prospect:list')
        else:
            messages.error(request, 'Unable to update Point of Contact. Try again.')

        context = {
            'title': 'Edit Point of Contact',
            'prospect_formset': prospect_formset,
            'prospect_instance': prospect_instance,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)