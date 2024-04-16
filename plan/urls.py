from django.urls import path
from plan import actions

app_name = 'plan'

urlpatterns = [
    path('ajax/plan-amount/', actions.get_plan_amount, name='get-plan-amount'),
]
