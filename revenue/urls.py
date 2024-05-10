from django.urls import path
from revenue import views

app_name = 'revenue'

urlpatterns = [
    path('overview/', views.RevenueDashboardViewView.as_view(), name='overview'),
]
