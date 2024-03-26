from django.urls import path
from contact import views
from contact import actions

app_name = "contact"

urlpatterns = [
    path("list/", views.ContactListView.as_view(), name="list"),
    path("create/", views.ContactCreateView.as_view(), name="create"),
    path("edit/<uuid:contact_id>/", views.ContactEditView.as_view(), name="edit"),

    path("delete/<uuid:contact_id>/", actions.delete_contact, name="delete"),
]
