from django.shortcuts import render
from django import forms
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
            dur=form.cleaned_data['duration']
            amt=form.cleaned_data['amount']
            data=planModels.plan_info(plan_name=pn,no_of_members=no,duration=dur,amount=amt)
            data.save()
            

        else:
             form = planForms.pl_info()
    return render(request, 'customer/form_plan.html', {'form': form})
# Create your views here.
