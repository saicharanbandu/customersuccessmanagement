from django.shortcuts import render,redirect
from customer import forms as customerForms
from django.urls import reverse

def index(request):
    return render(request,'customer/index.html')

def customer_info_view(request):
    form = customerForms.CustomerInfo()

    if request.method == "POST":
        form = customerForms.CustomerInfo(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('plan:plan_info_view'))
        else:
             form = customerForms.CustomerInfo()
    return render(request, 'customer/form_customer.html', {'form': form})
