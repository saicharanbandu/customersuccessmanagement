from django.urls import path
from . import views

app_name = 'prospect'

urlpatterns = [
    path('list/', views.ProspectsListView.as_view(), name='list'),
    path('create/', views.ProspectCreateView.as_view(), name='create'),

]
 