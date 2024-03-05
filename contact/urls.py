from django.urls import path
from contact import views

app_name = "contact"

urlpatterns = [
    path("create/", views.ContactCreateView.as_view(), name="create"),
    path("list/", views.ContactListView.as_view(), name="list"),
]
