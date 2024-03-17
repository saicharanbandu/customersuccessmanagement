from plan import models as planModels
from django.http import  JsonResponse



def get_plan_amount(request):
    plan_id = request.GET.get('plan_id')
    duration = request.GET.get('duration')

    monthly_amount = planModels.Tariff.objects.get(uuid=plan_id).amount
    payable_amount = monthly_amount * int(duration)
    
    response_data = {
        'payable_amount':payable_amount
    }
    return JsonResponse(response_data)
