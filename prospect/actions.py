from prospect import models as prospectModels, forms as prospectForms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse


@login_required
def update_remarks_ajax(request, prospect_id):
    template = 'prospect/_partials/_remarks_form.html'
    prospect_profile = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
    
    if request.method == 'GET':
        prospect_remarks_form = prospectForms.ProspectRemarksForm(instance=prospect_profile)
        context = {
            'prospect': prospect_profile,
            'prospect_remarks_form': prospect_remarks_form,
        }
        return render(request, template, context)
    
    if request.method == 'POST':
        prospect_remarks_form = prospectForms.ProspectRemarksForm(request.POST, instance=prospect_profile)
        if prospect_remarks_form.is_valid() :
            prospect_remarks_form.save()
            messages.success(request, 'Remarks for prospect has been successfully updated')
            return redirect(reverse('prospect:list'))
        else:
            messages.error(request, 'Remarks update unsuccessful. Try Again!')
            return redirect(reverse('prospect:list'))

@login_required
def update_customer_relationship_manager(request, prospect_id):
    template = 'prospect/_partials/_crm_form.html'
    prospect_profile = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
    
    if request.method == 'GET':
        prospect_crm_form = prospectForms.ProspectManagerForm()
        context = {
            'prospect': prospect_profile,
            'prospect_crm_form': prospect_crm_form,
        }
        return render(request, template, context)
    
    if request.method == 'POST':
        prospect_crm_form = prospectForms.ProspectManagerForm(request.POST)
        print(prospect_crm_form.errors)
        if prospect_crm_form.is_valid():
            prospect_profile.manager = prospect_crm_form.cleaned_data['manager']
            prospect_profile.save()
            messages.success(request, 'CRM for prospect has been successfully reassigned')
            return redirect(reverse('prospect:list'))
        else:
            messages.error(request, 'Unable to reassing CRM for prospect. Try Again!')
            return redirect(reverse('prospect:list'))

@login_required
def update_status(request, prospect_id):
    if request.method == 'POST':
        prospect_status_form = prospectForms.ProspectStatusForm()
        prospect_status_form.save()
        messages.success(request, 'Contact has been successfully deleted')
    else:
        messages.error(request,'Unsuccessful, try again')