from django.urls import path
from plan import views

app_name = 'plan'

urlpatterns = [
    path('ajax/plan-amount', views.get_plan_amount, name='get-plan-amount')
]
