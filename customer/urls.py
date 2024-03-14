from django.urls import path
from . import views as customerViews

app_name = 'customer'

urlpatterns = [
    path('ajax/load-states/', customerViews.load_states, name='ajax-load-states'),
    
    path('onboard', customerViews.CustomerOnboardingView.as_view(), name='onboard'),
    path('select-plan/<customer_id>', customerViews.CustomerSelectPlanView.as_view(), name='select-plan'),
    path('customer/<uuid:customer_id>/edit/', customerViews.CustomerEditView.as_view(), name='customer_edit'),
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    path('customer/<uuid:customer_id>/user/create/', customerViews.UserCreateView.as_view(), name='user-create'),
    path('customer/<uuid:customer_id>/user/add/', customerViews.AnotherUserCreateView.as_view(), name='user-add'),
]   
