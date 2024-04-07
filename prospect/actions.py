from prospect import models as prospectModels, forms as prospectForms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from tabernacle_customer_success import constants
from customer import models as customerModels
from datetime import date

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
    template = 'prospect/_partials/_status_form.html'
    prospect_profile = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
    prospect_status = prospectModels.StatusHistory.objects.filter(prospect_id=prospect_id).order_by('-updated_at')
    
    if request.method == 'GET':
        prospect_status_form = prospectForms.ProspectStatusForm(initial={'prospect': prospect_profile})

        context = {
            'prospect': prospect_profile,
            'prospect_status_form': prospect_status_form,
        }
        if prospect_status.exists():
            context.update({'prospect_status': prospect_status.first()})
            
        return render(request, template, context)
    
    if request.method == 'POST':
        prospect_status_form = prospectForms.ProspectStatusForm(request.POST)
        
        if prospect_status_form.is_valid():
            prospect_status_form.save()
            prospect_profile.status = prospect_status_form.cleaned_data['status']
            prospect_profile.save()

            if prospect_profile.status == constants.ACCEPTED:
                try:
                    customerModels.Profile.objects.get(prospect_id=prospect_id)
                except:
                    customerModels.Profile.objects.create(prospect_id=prospect_id)

            messages.success(request, 'Status for prospect successfully changed')
            return redirect(reverse('prospect:list'))
        else:
            messages.error(request, 'Unable to change status for prospect. Try Again!')
            return redirect(reverse('prospect:list'))
        

@login_required
def get_status_options(request):
    prospect_status_form = prospectForms.ProspectStatusForm(initial={'date': date.today()})
    
    status = request.GET.get('status')
    
    if status == constants.INITIATED:
        template = 'prospect/_partials/_option_initiated_form.html'
    
    if status == constants.MEETING_SCHEDULED:
        template = 'prospect/_partials/_option_meeting_scheduled_form.html'
    
    if status == constants.AWAITING:
        template = 'prospect/_partials/_option_awaiting_form.html'
    
    if status == constants.ACCEPTED:
        template = 'prospect/_partials/_option_accepted_form.html'
    
    if status == constants.REJECTED:
        template = 'prospect/_partials/_option_rejected_form.html'


    context = {
        'prospect_status_form': prospect_status_form
    }
    return render(request, template, context)


@login_required
def get_prospect_remarks(request, prospect_id):
    template = 'prospect/_partials/_remarks_view.html'
    prospect_profile = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
    context = {
        'prospect': prospect_profile
    }
    return render(request, template, context)


@login_required
def get_prospect_info(request, prospect_id):
    template = 'prospect/_partials/_info_view.html'
    prospect_profile = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
    context = {
        'prospect': prospect_profile
    }
    return render(request, template, context)


@login_required
def delete_prospect(request, prospect_id):
    if request.method == 'POST':
        prospect = prospectModels.Profile.objects.get(uuid=prospect_id)
        prospect.delete()
        messages.success(request, 'Prospect has been successfully deleted')
        return redirect(reverse('prospect:list'))
    else:
        messages.error(request,'Unsuccessful, try again')