from django.urls import path
from . import views

app_name = 'prospect'

urlpatterns = [
    path('list/', views.ProspectsListView.as_view(), name='list'),
    path('create/', views.ProspectCreateView.as_view(), name='create'),
    path('<uuid:prospect_id>/edit/', views.ProspectEditView.as_view(), name='edit'),
   path('<uuid:prospect_id>/update_poc/',
         views.UpdatePointOfContactView.as_view(),
         name='update_poc'),
]
