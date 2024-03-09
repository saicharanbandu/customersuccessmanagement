from django.urls import path
from . import views as customerViews

app_name = 'customer'

urlpatterns = [
    path('ajax/load-states/', customerViews.load_states, name='ajax-load-states'),
    
    path('create', customerViews.CustomerCreateView.as_view(), name='create'),
    path('select-plan/<customer_id>', customerViews.CustomerSelectPlanView.as_view(), name='select-plan'),
    path('customer/<uuid:customer_id>/edit/', customerViews.CustomerEditView.as_view(), name='customer_edit'),
    path('list/', customerViews.CustomerListView.as_view(), name='list'),

]   
