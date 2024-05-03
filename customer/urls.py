from django.urls import path
from . import views as customerViews
from . import actions as customerActions

app_name = 'customer'

urlpatterns = [
    path('list/', customerViews.CustomerListView.as_view(), name='list'),
    path('<uuid:customer_id>/onboard/', customerViews.CustomerOnboardingView.as_view(), name='onboard-customer'),
    path('<uuid:customer_id>/select-plan/', customerViews.OnboardingPlanView.as_view(), name='onboard-select-plan'),

    path('<uuid:customer_id>/user/create/', customerViews.OnboardingUserView.as_view(), name='onboard-user-create'),
    path('<uuid:customer_id>/user/create/next/', customerViews.OnboardingUserView.as_view(), name='onboard-user-create-next'),

    path('<uuid:customer_id>/user/s', customerViews.CustomerUsersView.as_view(), name='users'),
    path('<uuid:customer_id>/collaborators/add', customerViews.AddCollaboratorView.as_view(), name='add-collaborator'),
    path('<uuid:customer_id>/collaborators/edit/<uuid:collaborator_id>', customerViews.EditCollaboratorView.as_view(), name='edit-collaborator'),
    path('<uuid:customer_id>/collaborators/delete/<uuid:collaborator_id>', customerActions.delete_collaborator, name='delete-collaborator'),
    path('<uuid:customer_id>/user/create/more/', customerViews.UserCreateView.as_view(), name='user-create'),

    path('<uuid:customer_id>/plan/update/', customerViews.ChangePlanView.as_view(), name='plan-update'),


    path('<uuid:customer_id>/info/update/', customerViews.CustomerEditView.as_view(), name='update-info'),

    path('<uuid:prospect_id>/crm/update/', customerActions.update_customer_success_manager, name='update-csm-ajax'),

    path('<uuid:customer_id>/info/', customerActions.get_customer_info, name='get-customer-info'),
    path('<uuid:customer_id>/poc/', customerActions.get_poc, name='get-poc'),

    path("<uuid:customer_id>/delete/", customerActions.delete_customer, name="delete"),
    path('ajax/plan-options/', customerActions.get_plan_options, name='get-plan-options'),

    path('calendar', customerViews.CalendarSample.as_view(), name='sample'),


]   
