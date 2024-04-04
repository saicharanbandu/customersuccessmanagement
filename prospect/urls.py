from django.urls import path
from . import views
from . import actions

app_name = 'prospect'

urlpatterns = [
    path('list/', views.ProspectsListView.as_view(), name='list'),
    path('create/', views.ProspectCreateView.as_view(), name='create'),
    path('<uuid:prospect_id>/edit/', views.ProspectEditView.as_view(), name='edit'),

    path('<uuid:poc_id>/update_poc/<uuid:prospect_id>/', views.UpdatePointOfContactView.as_view(), name='update_poc'),

    path('<uuid:prospect_id>/update/remarks/', actions.update_remarks_ajax, name='update-remarks-ajax'),
    path('<uuid:prospect_id>/update/crm/', actions.update_customer_relationship_manager, name='update-crm-ajax'),
    path('<uuid:prospect_id>/update/status/', actions.update_status, name='update-status'),
]
