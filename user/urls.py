from django.urls import path
from user import views
app_name = 'user'

urlpatterns = [
 path("create/", views.UserCreateView.as_view(), name="create"),
 path("list/", views.UserListView.as_view(), name="list"),
 path("<uuid:profile_id>/edit/", views.UserEditView.as_view(), name="edit"),
 path("details/", views.LoggedUserEditView.as_view(), name="details"),
]
 