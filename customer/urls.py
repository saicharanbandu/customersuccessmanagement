from django.urls import path
from . import views as customerViews
from . import actions as customerActions

app_name = 'customer'

urlpatterns = [
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    path('onboard/', customerViews.CustomerOnboardingView.as_view(), name='onboard'),
    path('select-plan/<uuid:customer_id>/', customerViews.CustomerSelectPlanView.as_view(), name='select-plan'),

    path('<uuid:customer_id>/user/create/', customerViews.UserCreateView.as_view(), name='user-create'),
    path('<uuid:customer_id>/user/add/', customerViews.AnotherUserCreateView.as_view(), name='user-add'),

    path('<uuid:customer_id>/edit/', customerViews.CustomerEditView.as_view(), name='edit-info'),

    path('<uuid:customer_id>/info/', customerActions.get_customer_info, name='get-customer-info'),

]   
