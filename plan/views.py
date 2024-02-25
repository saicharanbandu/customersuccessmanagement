from django.shortcuts import render,redirect
from django import forms
from django.urls import reverse
from  plan import forms as planForms
from plan import models as planModels

# Create your views here.

def plan_info_view(request):
    form=planForms.pl_info()
    if request.method == "POST":
        form=planForms.pl_info(request.POST)
        if form.is_valid():
            pn=form.cleaned_data['plan_name']
            no=form.cleaned_data['no_of_members']
            # dur=form.cleaned_data['duration']
            amt=form.cleaned_data['amount']
            data=planModels.plan_info(plan_name=pn,no_of_members=no,amount=amt)
            data.save()
            return redirect(reverse('user:user_view'))

        else:
             form = planForms.pl_info()
    return render(request, 'customer/form_plan.html', {'form': form})

def load_numbers(request):
    plan_name_id = request.GET.get('plan_name_id')
    
    if plan_name_id is None:
        print("The country_id is empty")
    numbers = planModels.Number.objects.filter(type_id=plan_name_id).order_by('num')
   
    print(numbers)
    return render(request, 'customer/number_dropdown_list.html', {'numbers': numbers})

def load_amount(request):
    plan_name_id = request.GET.get('plan_name_id')
    no_of_members = request.GET.get('no_of_members')
    duration = request.GET.get('duration')
    amount = planModels.Amount.objects.get(type_id=plan_name_id,num_id=no_of_members,dur_id=duration).amt
    return {'amount':amount}