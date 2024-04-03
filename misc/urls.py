from django.urls import path
from . import views, actions

app_name = 'misc'

urlpatterns = [
    path('load-states/', actions.load_states, name='ajax-load-states'),
]
 