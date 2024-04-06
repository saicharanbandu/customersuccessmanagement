from django.urls import path
from . import views
from . import actions

app_name = 'prospect'

urlpatterns = [
    path('list/', views.ProspectsListView.as_view(), name='list'),
    path('create/', views.ProspectCreateView.as_view(), name='create'),
    path('<uuid:prospect_id>/edit/', views.ProspectEditView.as_view(), name='edit'),

    path('<uuid:prospect_id>/poc/update/', views.UpdatePointOfContactView.as_view(), name='update-poc'),

    path('<uuid:prospect_id>/remarks/update/', actions.update_remarks_ajax, name='update-remarks-ajax'),
    path('<uuid:prospect_id>/crm/update/', actions.update_customer_relationship_manager, name='update-crm-ajax'),
    path('<uuid:prospect_id>/status/update/', actions.update_status, name='update-status-ajax'),
    path('get-status-options/', actions.get_status_options, name='get-status-options'),


    path('<uuid:prospect_id>/get-prospect-remarks/', actions.get_prospect_remarks, name='get-prospect-remarks'),
    path('<uuid:prospect_id>/get-prospect-info/', actions.get_prospect_info, name='get-prospect-info'),
    path('<uuid:prospect_id>/delete/', actions.delete_prospect, name='delete'),
  
]
