from django.urls import path
from contact import views
from contact import actions

app_name = "contact"

urlpatterns = [
    path("list/", views.ContactListView.as_view(), name="list"),
    path("create/", views.ContactCreateView.as_view(), name="create"),
    path("<uuid:contact_id>/edit/", views.ContactEditView.as_view(), name="edit"),

    path("<uuid:contact_id>/delete/", actions.delete_contact, name="delete"),
]
