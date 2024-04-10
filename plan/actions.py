from plan import models as planModels
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tabernacle_customer_success import helper
from decimal import Decimal, ROUND_HALF_UP

@login_required
def get_plan_amount(request):
    plan_id = request.GET.get('plan_id')
    is_yearly = request.GET.get('is_yearly')

    monthly_amount = planModels.Tariff.objects.get(uuid=plan_id).amount
    
    if is_yearly == 'true':
        discount_percentage = 20

        discount_percentage_decimal = Decimal(discount_percentage)
        discount_amount = (discount_percentage_decimal / Decimal(100)) * (monthly_amount * 12)
        discounted_price = (monthly_amount * 12) - discount_amount
        payable_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    else:
        payable_amount = monthly_amount

    response_data = {
        'payable_amount': helper.formatINR(payable_amount)
    }
    return JsonResponse(response_data)

