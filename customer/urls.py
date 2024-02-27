from django.urls import path
from customer import views

app_name = 'customer'
urlpatterns = [
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),

    path('create', views.CustomerCreateView.as_view(), name='create'),
    path('select-plan/<customer_id>', views.CustomerSelectPlanView.as_view(), name='select_plan'),


]   
