from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from . import models as customerModels, forms as customerForms
from misc import models as miscModels
from plan import models as planModels

from tabernacle_customer_success import constants

class CustomerCreateView(View):
    template_name = 'customer/create_view.html'
    title = 'Crustomer Information'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm(request.POST)
        
        if customer_info_form.is_valid():
            customer_info_object = customer_info_form.save()
            return redirect(reverse('customer:select-plan', kwargs={'customer_id': customer_info_object.uuid }))
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form
        }
        return render(request, self.template_name, context)



class CustomerSelectPlanView(View):
    template_name = 'customer/select_plan.html'
    title = 'Select Plan'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        customer_plan_form = customerForms.CustomerPlanForm()
        plan_options_form = customerForms.PlanOptionsForm()
    
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_plan_form': customer_plan_form,
            'plan_options_form': plan_options_form,
            'customer_id': customer_id
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        plan_options_form = customerForms.PlanOptionsForm(request.POST)
        
        if plan_options_form.is_valid():
            
            plan_type = plan_options_form.cleaned_data['plan_type']
            member_size = plan_options_form.cleaned_data['member_size']
            duration = plan_options_form.cleaned_data['duration']

            subscription_plan = planModels.SubscriptionPlan.objects.get(plan_type=plan_type, member_size=member_size)
            customerModels.CustomerPlan.objects.create(customer_id=customer_id, subscription_plan=subscription_plan, duration_in_months=duration)
            return redirect(reverse('customer:list'))
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'plan_options_form': plan_options_form
        }
        return render(request, self.template_name, context)

def load_states(request):
    country_id = request.GET.get('country_id')
    states = miscModels.State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'customer/state_dropdown_list.html', {'states': states})

            
class CustomerListView(ListView):
    model = customerModels.CustomerInfo
    template_name = 'customer/list_view.html'
    title = 'Customer List'
    active_tab = 'customer'
    context_object_name = 'customers'

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if (page_limit == 'all'):
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
