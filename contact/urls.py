from django.urls import path
from contact import views 
from django.contrib import admin  
from django.urls import path   
from django.conf import settings  
from django.conf.urls.static import static
app_name = 'contact'
urlpatterns = [
    path('',views.index,name='index'),
    path('form/',views.ContactCreateView.as_view(),name='contact_create_view'),
     path('list/', views.ContactListView.as_view(), name='contact_list'),
]
