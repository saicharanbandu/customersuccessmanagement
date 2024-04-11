from django.urls import path
from . import views as customerViews
from . import actions as customerActions

app_name = 'customer'

urlpatterns = [
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    path('<uuid:customer_id>/onboard/', customerViews.CustomerOnboardingView.as_view(), name='onboard'),
    path('<uuid:customer_id>/select-plan/', customerViews.CustomerSelectPlanView.as_view(), name='select-plan'),

    path('<uuid:customer_id>/user/create/', customerViews.UserCreateView.as_view(), name='user-create'),
    path('<uuid:customer_id>/user/create/next', customerViews.UserCreateView.as_view(), name='user-create-next'),

    path('<uuid:customer_id>/info/update/', customerViews.CustomerEditView.as_view(), name='update-info'),

    path('<uuid:prospect_id>/crm/update/', customerActions.update_customer_success_manager, name='update-csm-ajax'),

    path('<uuid:customer_id>/info/', customerActions.get_customer_info, name='get-customer-info'),
    path('<uuid:customer_id>/poc/', customerActions.get_poc, name='get-poc'),

    path("<uuid:customer_id>/delete/", customerActions.delete_customer, name="delete"),
    path('ajax/plan-options/', customerActions.get_plan_options, name='get-plan-options')

]   
