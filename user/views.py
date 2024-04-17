from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from user import forms as userForms
from user import models as userModels
from django.contrib import messages
from django.views.generic import ListView
from tabernacle_customer_success import constants
from django.db.models import Q

class UserCreateView(View):
    title = 'Create User'
    template_name = 'user/create_view.html'
    active_tab = 'user'
    def get(self, request, *args, **kwargs):
        user_form = userForms.UserInfo()
        profile_form = userForms.UserProfile()
        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "user_form": user_form,
            "profile_form": profile_form,

        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = userForms.UserInfo(request.POST)
        profile_form = userForms.UserProfile(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_instance = user_form.save()
            user_instance = get_object_or_404(userModels.User, uuid=user_instance.uuid)
            profile_form_instance = profile_form.save(commit=False)
            profile_form_instance.user = user_instance
            profile_form_instance.save()

            messages.success(request, 'User has been successfully created')
            return redirect(reverse("user:list"))
        else:
            context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "user_form": user_form,
            "profile_form": profile_form,
        }
        print(user_form.errors)
        print(profile_form.errors)
        messages.error(request, 'Failed to add user')
        return render(request, self.template_name, context)

class UserListView(ListView):
    model = userModels.Profile
    title = "User Directory"
    active_tab = "profile"
    template_name = "user/list_view.html"
    context_object_name = "profiles"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        
        if search_query:
            queryset = queryset.filter(
                Q(user__full_name__icontains=search_query)| Q(user__full_name__icontains=" " + search_query)
            )
        return queryset.order_by('user__full_name')
    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get("page_limit", constants.PAGINATION_LIMIT)
        if page_limit == "all":
            page_limit = len(queryset)
        return self.request.GET.get("paginate_by", page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        more_context = {
            "title": self.title,
            "active_tab": self.active_tab,
        }
       
        return context
    
class UserEditView(View):
    template_name = "user/edit_view.html"
    title = "Edit User"
    active_tab = "user"

    def get(self, request, profile_id, *args, **kwargs):
        user = get_object_or_404(userModels.Profile, uuid=profile_id)
        user_form = userForms.UserInfo(instance=user.user)
        profile_form = userForms.UserProfile(instance=user)

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "profile_form": profile_form,
            "user_form": user_form,
            "profile_id": profile_id,
        }

        return render(request, self.template_name, context)

    def post(self, request, profile_id, *args, **kwargs):
        user_profile = get_object_or_404(userModels.Profile, uuid=profile_id)
        user_instance = user_profile.user  # Get the related user instance
    
        user_form = userForms.UserInfo(request.POST, instance=user_instance)
        profile_form = userForms.UserProfile(request.POST, request.FILES, instance=user_profile)
    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Contact has been successfully edited')
            return redirect(reverse("user:list"))
        else:
            context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "user_form": user_form,
            "profile_form": profile_form,
            "profile_id": profile_id,
        }
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Contact has not been successfully edited')
            return render(request, self.template_name, context)
        
class LoggedUserEditView(View):
    template_name = "user/edit_view.html"
    title = "Edit User"
    active_tab = "user"

    def get(self, request, *args, **kwargs):
        print(request.user)
        profile_id=request.user.uuid
        print(profile_id)
        user = get_object_or_404(userModels.Profile, user=profile_id)
        user_form = userForms.UserInfo(instance=user.user)
        profile_form = userForms.UserProfile(instance=user)

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "profile_form": profile_form,
            "user_form": user_form,
            "profile_id": profile_id,
        }

        return render(request, self.template_name, context)

    def post(self, request, profile_id, *args, **kwargs):
        user_profile = get_object_or_404(userModels.Profile, uuid=profile_id)
        user_instance = user_profile.user  # Get the related user instance
    
        user_form = userForms.UserInfo(request.POST, instance=user_instance)
        profile_form = userForms.UserProfile(request.POST, request.FILES, instance=user_profile)
    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Contact has been successfully edited')
            return redirect(reverse("user:list"))
        else:
            context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "user_form": user_form,
            "profile_form": profile_form,
            "profile_id": profile_id,
        }
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Contact has not been successfully edited')
            return render(request, self.template_name, context)