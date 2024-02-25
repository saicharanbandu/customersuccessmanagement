from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('list', views.ContactListView.as_view(), name='list'),
    path('create', views.ContactCreateView.as_view(), name='create'),

]
