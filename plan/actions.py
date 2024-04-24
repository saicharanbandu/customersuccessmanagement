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

    tariff = planModels.Tariff.objects.get(uuid=plan_id)
    monthly_amount = tariff.amount
    
    if is_yearly == 'true':
        discount_percentage = 15

        discount_percentage_decimal = Decimal(discount_percentage)
        discount_amount = (discount_percentage_decimal / Decimal(100)) * (monthly_amount * 12)
        discounted_price = (monthly_amount * 12) - discount_amount
        payable_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        tariff_selected = tariff.name + 'Plan (Yearly)'
        monthly_amount = helper.formatINR((Decimal(100) / Decimal(100)) * (monthly_amount * 12))
    else:
        payable_amount = monthly_amount
        tariff_selected = tariff.name + 'Plan (Monthly)'
        monthly_amount = helper.formatINR(monthly_amount)

    response_data = {
        'tariff_selected': tariff_selected,
        'monthly_amount': monthly_amount,
        'payable_amount': helper.formatINR(payable_amount)
    }
    return JsonResponse(response_data)

