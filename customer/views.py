from django.shortcuts import render,redirect
from django import forms
from customer import forms
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'customer/index.html')

def customer_info_view(request):
    form=forms.Customer_info()
    if request.method == "POST":
        form=Customer_info(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('plan:plan_info_view'))

        else:
             form = Customer_info()
    return render(request, 'customer/form_customer.html', {'form': form})
