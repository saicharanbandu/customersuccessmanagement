from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('form2/',views.user_view,name='user_view'),
]
