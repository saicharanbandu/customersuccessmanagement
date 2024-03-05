from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View

from customer import models as customerModels, forms as customerForms
from misc import models as miscModels
from plan import models as planModels

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
            print(customer_info_object.uuid)
            return redirect(reverse('customer:select_plan', kwargs={'customer_id': customer_info_object.uuid }))
        
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
            customerModels.CustomerPlan.objects.create(customer_id=customer_id, plan=subscription_plan, duration_months=duration)
            return redirect(reverse('customer:create'))
        
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'plan_options_form': plan_options_form
        }
        return render(request, self.template_name, context)

def load_states(request):
    country_id = request.GET.get('country_id')
    if country_id is None:
        print("The country_id is empty")
    states = miscModels.State.objects.filter(country_id=country_id).order_by('name')
    print(states)
    return render(request, 'customer/state_dropdown_list.html', {'states': states})

