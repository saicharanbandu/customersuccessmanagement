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
from .filters import ProfileFilter
from django.db.models import Q
from customer import models as customerModels

@method_decorator(login_required, name='dispatch')
class ProspectsListView(ListView):
    model = prospectModels.Profile
    context_object_name = 'prospects'
    template_name = 'prospect/list_view.html'
    filterset_class = ProfileFilter
    title="Prospect List"
    active_tab="prospect"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        sort = self.request.GET.get("sort", "")
        status = self.request.GET.get("status", "")
        print("Status:", status)
        if search_query:
            queryset = queryset.filter(
                Q(name__istartswith=search_query) |
                Q(name__icontains=' ' + search_query)
            )
        if status:
            print("Filtering queryset by status:", status)
            queryset = queryset.filter(status=status)

        if sort:
            if sort == "name_asc":
                print("a-z")
                queryset = queryset.order_by("name")
            elif sort == "name_desc":
                print("z-a")
                queryset = queryset.order_by("-name")
            elif sort == "crm_name_asc":
                queryset = queryset.order_by("-created_at")
            elif sort == "crm_name_desc":
                queryset = queryset.order_by("created_at")
            elif sort == "updated_newest":
                queryset = queryset.order_by("-updated_at")
            elif sort == "updated_oldest":
                queryset = queryset.order_by("updated_at")
        return queryset
        

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sort_options = {
            "name_asc": "Customer Name (A-Z)",
            "name_desc": "Customer Name (Z-A)",
            "crm_name_asc": "CRM Name (A-Z)",
            "crm_name_desc": "CRM Name (Z-A)",
            "updated_newest": "Record Updated (Newest First)",
            "updated_oldest": "Record Updated (Oldest First) ",
        }
        filter_form = ProfileFilter(self.request.GET, queryset=self.get_queryset())
        context.update({
            "title": self.title,
            "active_tab": self.active_tab,
            "sort_options": sort_options,
            "prospect_filter": filter_form,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(
            prefix='prospect', initial={'manager': request.user}
        )

        PointOfContactFormSet = formset_factory(
            prospectForms.PointOfContactForm,
            min_num=1,
            validate_min=True,
            extra=1,
            can_delete=True,
        )
        poc_formset = PointOfContactFormSet()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(
            request.POST, prefix='prospect'
        )
        PointOfContactFormSet = formset_factory(
            prospectForms.PointOfContactForm, extra=2
        )
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
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(
            instance=prospect, prefix='prospect'
        )

        has_customer = True if customerModels.Profile.objects.filter(prospect=prospect).exists() else False

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'has_customer': has_customer
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(
            request.POST, instance=prospect_instance, prefix='prospect'
        )

        if prospect_form.is_valid():
            prospect_form.save()
            messages.success(
                request, 'Prospect information has been successfully updated'
            )
            return redirect('prospect:list')
        else:
            messages.error(
                request, 'Unsuccessful! Please check the form and try again.'
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UpdatePointOfContactView(View):
    template_name = 'prospect/edit_poc.html'
    title = 'Edit Point of Contact'
    PointOfContactFormSet = modelformset_factory(
        prospectModels.PointOfContact,
        form=prospectForms.PointOfContactForm,
        extra=2,
        exclude=(),
        min_num=0,
        max_num=2,
        can_delete=True,
    )

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
                
        poc_formset = self.PointOfContactFormSet(
            queryset=prospect.prospect_poc.all(),
        )

        context = {
            'title': self.title,
            'poc_formset': poc_formset,
            'prospect': prospect,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)

        poc_formset = self.PointOfContactFormSet(
            request.POST, queryset=prospect.prospect_poc.all()
        )

        if poc_formset.is_valid():
            for form in poc_formset:
                if form.cleaned_data:
                    if form.is_empty() and form.instance.pk:
                        form.instance.delete()
                    else:
                        point_of_contact_info = form.save(commit=False)
                        point_of_contact_info.prospect = prospect
                        point_of_contact_info.save()
            messages.success(request, 'Point of Contact updated successfully')
            return redirect('prospect:list')
        else:
            messages.error(request, 'Unable to update Point of Contact. Try again.')

        context = {
            'title': self.title,
            'poc_formset': poc_formset,
            'prospect': prospect,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)
