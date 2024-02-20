from django.urls import path
from plan import views

app_name = 'plan'

urlpatterns = [
    path('form1/',views.plan_info_view,name='plan_info_view'),
]
