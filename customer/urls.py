from django.urls import path
from . import views as customerViews

app_name = 'customer'

urlpatterns = [
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    path('onboard', customerViews.CustomerOnboardingView.as_view(), name='onboard'),
    path('select-plan/<uuid:customer_id>', customerViews.CustomerSelectPlanView.as_view(), name='select-plan'),

    path('customer/<uuid:customer_id>/user/create/', customerViews.UserCreateView.as_view(), name='user-create'),
    path('customer/<uuid:customer_id>/user/add/', customerViews.AnotherUserCreateView.as_view(), name='user-add'),

    path('customer/<uuid:customer_id>/edit/', customerViews.CustomerEditView.as_view(), name='customer_edit'),
]   
