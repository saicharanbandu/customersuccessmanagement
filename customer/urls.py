from django.urls import path
from customer import views
urlpatterns = [
path('',views.index,name='index'),
    path('form/',views.customer_info_view,name='customer_info_view'),
]
