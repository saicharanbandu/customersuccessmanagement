from django.shortcuts import render,redirect
from customer import forms as customerForms
from django.urls import reverse
from customer import models as customerModel

def index(request):
    return render(request,'customer/index.html')

def customer_info_view(request):
    form = customerForms.CustomerInfo()

    if request.method == "POST":
        form = customerForms.CustomerInfo(request.POST)
        
        if form.is_valid():
            
            ln=form.cleaned_data['legal_name']
            dn=form.cleaned_data['display_name']
            sn=form.cleaned_data['short_name']
            add=form.cleaned_data['address']
            city=form.cleaned_data['city']
            country=form.cleaned_data['country']
            state=form.cleaned_data['state']
            zip=form.cleaned_data['zip_code']
            data=customerModel.CustomerInfo(legal_name=ln,display_name=dn,short_name=sn,address=add,city=city,country=country,state=state,zip_code=zip)
            
            data.save()
            
            return redirect(reverse('plan:plan_info_view'))
        else:
             form = customerForms.CustomerInfo()
    return render(request, 'customer/form_customer.html', {'form': form})

def load_states(request):
    country_id = request.GET.get('country_id')
    if country_id is None:
        print("The country_id is empty")
    states = customerModel.State.objects.filter(country_id=country_id).order_by('name')
    print(states)
    return render(request, 'customer/state_dropdown_list.html', {'states': states})