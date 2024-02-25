from django.urls import path
from plan import views

app_name = 'plan'

urlpatterns = [
    path('form1/',views.plan_info_view,name='plan_info_view'),
    path('ajax/load-numbers/', views.load_numbers, name='ajax_load_numbers'),
    path('ajax/load-amount/', views.load_amount, name='ajax_load_amount')
]
