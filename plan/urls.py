from django.urls import path
from plan import views

app_name = 'plan'

urlpatterns = [
    path('ajax/load-numbers/', views.load_numbers, name='ajax_load_numbers'),
    path('ajax/load-amount/', views.load_amount, name='ajax_load_amount')
]
