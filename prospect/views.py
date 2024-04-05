from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from tabernacle_customer_success import constants
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Q


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(prefix='prospect', initial={'manager': request.user})
        
        PointOfContactFormSet = formset_factory(prospectForms.PointOfContactForm, min_num=1, validate_min=True, extra=1, can_delete=True)
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
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
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


@method_decorator(login_required, name='dispatch')
class ProspectEditView(View):
    template_name = 'prospect/edit_view.html'
    title = 'Edit Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(instance=prospect_instance, prefix='prospect')

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(request.POST, instance=prospect_instance, prefix='prospect')
        
        if prospect_form.is_valid():
            prospect_form.save()
            
            messages.success(request, 'Prospect information has been successfully updated')
            return redirect('prospect:list')
        else:
            print(prospect_form.errors)
            
            messages.error(request, 'Unsuccessful! Please check the form and try again.')

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UpdatePointOfContactView(View):
    model = prospectModels.PointOfContact
    form_class = prospectForms.PointOfContactForm
    template_name = 'prospect/update_poc.html'
    PointOfContactFormSet = modelformset_factory(prospectModels.PointOfContact, form=prospectForms.PointOfContactForm, extra=0, exclude=())   

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        
        prospect_formset = self.PointOfContactFormSet(queryset=prospect_instance.prospect_poc.all())

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
        queryset=prospect_instance.prospect_poc.all()

        prospect_formset = self.PointOfContactFormSet(request.POST, queryset=queryset)
        print(prospect_formset.errors)
        if prospect_formset.is_valid():
            prospect_formset.save()
            messages.success(request, 'Point of Contact updated successfully')
            return redirect('prospect:view', ob=prospect_instance.slug)
        else:
            prospect_formset = self.PointOfContactFormSet(queryset=prospect_instance.prospect_poc.all(), prefix='form')
            messages.error(request, 'Unable to update Point of Contact. Try again.')

        context = {
            'title': 'Edit Point of Contact',
            'prospect_formset': prospect_formset,
            'prospect_instance': prospect_instance,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)
