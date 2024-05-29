from django.urls import path
from . import views as customerViews
from . import actions as customerActions
from customer import views

app_name = 'customer'

urlpatterns = [
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    
    path('<uuid:customer_id>/onboard/', customerViews.OnboardingCustomerView.as_view(), name='onboard-customer'),
    path('<uuid:customer_id>/select-plan/', customerViews.OnboardingPlanView.as_view(), name='onboard-select-plan'),
    path('<uuid:customer_id>/user/create/', customerViews.OnboardingUserView.as_view(), name='onboard-user-create'),
    path('<uuid:customer_id>/user/create/next/', customerViews.OnboardingUserView.as_view(), name='onboard-user-create-next'),

    path('<uuid:customer_id>/user/s', customerViews.CustomerCollaboratorsView.as_view(), name='users'),
    path('<uuid:customer_id>/collaborators/add', customerViews.AddCollaboratorView.as_view(), name='add-collaborator'),
    path('<uuid:customer_id>/collaborators/edit/<uuid:collaborator_id>', customerViews.EditCollaboratorView.as_view(), name='edit-collaborator'),
    
    path('<uuid:customer_id>/collaborators/delete/<uuid:collaborator_id>', customerActions.delete_collaborator, name='delete-collaborator'),

    path('<uuid:customer_id>/plan/update/', customerViews.ChangePlanView.as_view(), name='plan-update'),


    path('<uuid:customer_id>/info/update/', customerViews.CustomerEditView.as_view(), name='update-info'),
    path('<uuid:customer_id>/record_payment/', customerViews.PaymentView.as_view(), name='record-payment'),
    path('<uuid:customer_id>/payment_list/', customerViews.PaymentListView.as_view(), name='payment_list'),
    path('<uuid:prospect_id>/crm/update/', customerActions.update_customer_success_manager, name='update-csm-ajax'),

    path('<uuid:customer_id>/info/', customerActions.get_customer_info, name='get-customer-info'),
    path('<uuid:customer_id>/poc/', customerActions.get_poc, name='get-poc'),
    path("<uuid:customer_id>/edit/<uuid:payment_id>/", customerViews.PaymentEditView.as_view(), name="edit-payment"),
    path("<uuid:customer_id>/delete/<uuid:payment_id>/", customerActions.delete_payment, name="delete_payment"),
    path('ajax/plan-options/', customerActions.get_plan_options, name='get-plan-options'),
    path('overview/', views.CustomerDashboardView.as_view(), name='overview'),

]   
