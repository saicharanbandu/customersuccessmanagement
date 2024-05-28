from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import models as customerModels
from prospect import models as prospectModels
from customer import forms as customerForms

import os

@login_required
def delete_customer(request, customer_id):
    if request.method == 'POST':
        customer = customerModels.Profile.objects.get(uuid=customer_id)
        try:
            if customer.profile_picture:
                os.remove(customer.profile_picture.path)
        except OSError:
            pass
        customer.delete()
        messages.success(request, 'Customer has been successfully deleted')
        return redirect(reverse('customer:list'))
    else:
        messages.error(request,'Unsuccessful, try again')
@login_required       
def delete_payment(request,customer_id, payment_id):
    print(request.POST)
    if request.method == 'POST':
        payment = customerModels.PaymentHistory.objects.get(uuid=payment_id)
        print(payment)
        payment.delete()
        messages.success(request, 'Payment has been successfully deleted')
        return redirect(reverse("customer:payment_list", kwargs={"customer_id": customer_id}))
    else:
        messages.error(request,'Unsuccessful, try again')

@login_required
def delete_collaborator(request, customer_id, collaborator_id):
    # if request.method == 'POST':
    collaborator = customerModels.User.objects.get(uuid=collaborator_id)
    collaborator.delete()
    messages.success(request, 'Customer has been successfully deleted')
    return redirect(reverse('customer:users', kwargs={'customer_id': customer_id}))
    # else:
        # messages.error(request,'Unsuccessful, try again')


@login_required
def get_customer_info(request, customer_id):
    template = 'customer/_partials/_info_view.html'
    customer_profile = customerModels.Profile.objects.get(uuid=customer_id)
    context = {
        'customer': customer_profile,
    }
    return render(request, template, context)



@login_required
def get_poc(request, customer_id):
    template = 'customer/_partials/_poc_view.html'
    customer_profile = customerModels.Profile.objects.get(uuid=customer_id)
    contacts = prospectModels.PointOfContact.objects.filter(prospect=customer_profile.prospect)
    context = {
        'customer': customer_profile,
        'contacts': contacts,
    }
    return render(request, template, context)



@login_required
def update_customer_success_manager(request, prospect_id):
    template = 'customer/_partials/_csm_form.html'
    customer_profile = get_object_or_404(customerModels.Profile, uuid=prospect_id)
    
    if request.method == 'GET':
        customer_csm_form = customerForms.CustomerManagerForm()
        context = {
            'customer': customer_profile,
            'customer_csm_form': customer_csm_form,
        }
        return render(request, template, context)
    
    if request.method == 'POST':
        customer_csm_form = customerForms.CustomerManagerForm(request.POST)
       
        if customer_csm_form.is_valid():
            customer_profile.manager = customer_csm_form.cleaned_data['manager']
            customer_profile.save()
            messages.success(request, 'CSM for prospect has been successfully reassigned')
            return redirect(reverse('customer:list'))
        else:
            messages.error(request, 'Unable to reassing CSM for prospect. Try Again!')
            return redirect(reverse('customer:list'))



@login_required
def get_plan_options(request):
    template = 'customer/_partials/_plan_options_form.html'
    plan_id = request.GET.get('plan_id')
    is_yearly = request.GET.get('is_yearly')
    plan_options_form = customerForms.SubscriptionPlanOptionsForm(initial={'plan': plan_id})
    context = {
        'plan_options_form': plan_options_form,
        'is_yearly': is_yearly
    }
    return render(request, template, context)