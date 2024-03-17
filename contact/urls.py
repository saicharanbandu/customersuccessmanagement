from django.urls import path
from contact import views

app_name = "contact"

urlpatterns = [
    path("list/", views.ContactListView.as_view(), name="list"),
    path("create/", views.ContactCreateView.as_view(), name="create"),
    path("edit/<uuid:contact_id>/", views.ContactEditView.as_view(), name="edit")
]
