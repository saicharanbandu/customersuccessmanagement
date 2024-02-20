from django.shortcuts import render
from django import forms
from  plan import forms

# Create your views here.

def plan_info_view(request):
    form=forms.pl_info()
    if request.method == "POST":
        form=Customer_info(request.POST)
        if form.is_valid():
            form.save(commit=True)
            

        else:
             form = pl_info()
    return render(request, 'customer/form_plan.html', {'form': form})
# Create your views here.
