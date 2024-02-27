from django.shortcuts import render,redirect
from django import forms
from django.urls import reverse
from  plan import forms as planForms
from plan import models as planModels
from django.http import  JsonResponse



def load_numbers(request):
    plan_type_id = request.GET.get('plan_type_id')
    
    plan_types = planModels.SubscriptionPlan.objects.filter(plan_type_id=plan_type_id).order_by('member_size__lower_limit')
    return render(request, 'customer/number_dropdown_list.html', {'plan_types': plan_types})



def load_amount(request):
    plan_type_id = request.GET.get('plan_type_id')
    member_size_id = request.GET.get('member_size_id')
    duration = request.GET.get('duration')

    monthly_amount = planModels.SubscriptionPlan.objects.get(plan_type_id=plan_type_id, member_size_id=member_size_id).amount
    payable_amount = monthly_amount * int(duration)
    
    response_data = {
        'payable_amount':payable_amount
    }
    return JsonResponse(response_data)
