from django.shortcuts import render
from django import forms
from user import forms as userForms
from user import models as userModels
# Create your views here.

def user_view(request):
    form=userForms.UserInfo()
    if request.method == "POST":
        form=userForms.UserInfo(request.POST)
        if form.is_valid():
            fn=form.cleaned_data['full_name']
            des=form.cleaned_data['designation']
            dail=form.cleaned_data['dailing_code']
            mob=form.cleaned_data['mobile_no']
            data=userModels.user_info(full_name=fn,designation=des,dailing_code=dail,mobile_no=mob)
            data.save()
            

        else:
             form = userForms.UserInfo()
    return render(request, 'customer/form_user.html', {'form': form})