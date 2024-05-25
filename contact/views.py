from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import ContactFilter
from . import models as contactModel, forms as contactForm

from tabernacle_customer_success import constants


@method_decorator(login_required, name='dispatch')
class ContactCreateView(View):
    template_name = "contact/create_view.html"
    title = "New Contact"
    active_tab = "contact"

    def get(self, request, *args, **kwargs):
        contact_form = contactForm.ContactForm(initial={'created_by': request.user})

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "contact_form": contact_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contact_info_form = contactForm.ContactForm(request.POST, request.FILES)
        if contact_info_form.is_valid():
            contact_info_form.save()
            messages.success(request, 'Contact has been successfully created')
            return redirect(reverse("contact:list"))
        else:
            contact_info_form = contactForm.ContactForm(request.POST, request.FILES)
            context = {
                "title": self.title,
                "active_tab": self.active_tab,
                "contact_info_form": contact_info_form,
            }
            messages.error(request, 'Contact has been successfully created')
            return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    model = contactModel.Contact
    filterset_class = ContactFilter
    title = "Contact Directory"
    active_tab = "contact"
    template_name = "contact/list_view.html"
    context_object_name = "contacts"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        sort = self.request.GET.get("sort", "")
        if search_query:
            queryset = queryset.filter(
                (
                    Q(name__istartswith=search_query)
                    | Q(name__icontains=" " + search_query)
                )
                | (
                    Q(organization__istartswith=search_query)
                    | Q(organization__icontains=" " + search_query)
                )
            )
        



        if sort:
            if sort == "name_asc":
                print("a-z")
                queryset = queryset.order_by("name")
            elif sort == "name_desc":
                print("z-a")
                queryset = queryset.order_by("-name")
            elif sort == "created_newest":
                queryset = queryset.order_by("-created_at")
            elif sort == "created_oldest":
                queryset = queryset.order_by("created_at")
            elif sort == "updated_newest":
                queryset = queryset.order_by("-updated_at")
            elif sort == "updated_oldest":
                queryset = queryset.order_by("updated_at")
        return queryset

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get("page_limit", constants.PAGINATION_LIMIT)
        if page_limit == "all":
            page_limit = len(queryset)
        return self.request.GET.get("paginate_by", page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_options = {
            "name_asc": "Customer Name (A-Z)",
            "name_desc": "Customer Name (Z-A)",
            "created_newest": "Contact Created (Newest First)",
            "created_oldest": "Contact Created (Oldest First)",
            "updated_newest": "Contact Updated (Newest First)",
            "updated_oldest": "Contact Updated (Oldest First) ",
        }
        filter_form = ContactFilter(self.request.GET, queryset=self.get_queryset())
        context.update({
            "title": self.title,
            "active_tab": self.active_tab,
            "sort_options": sort_options,
            "contact_filter": filter_form,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ContactEditView(View):
    template_name = "contact/edit_view.html"
    title = "Edit Contact"
    active_tab = "contact"

    def get(self, request, contact_id, *args, **kwargs):
        contact = get_object_or_404(contactModel.Contact, uuid=contact_id)
        contact_form = contactForm.ContactForm(instance=contact, initial={'updated_by': request.user})

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "contact_form": contact_form,
            "contact_id": contact_id,
        }

        return render(request, self.template_name, context)

    def post(self, request, contact_id, *args, **kwargs):
        contact = get_object_or_404(contactModel.Contact, uuid=contact_id)
        contact_info_form = contactForm.ContactForm(
            request.POST, request.FILES, instance=contact
        )
        if contact_info_form.is_valid():
            contact_info_form.save()
            return redirect(reverse("contact:list"))
        else:
            contact_info_form = contactForm.ContactForm(instance=contact)
            context = {
                "title": self.title,
                "active_tab": self.active_tab,
                "contact_info_form": contact_info_form,
                "contact_id": contact_id,
            }
            return render(request, self.template_name, context)
