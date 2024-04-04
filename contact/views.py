from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
    title = "Contact Directory"
    active_tab = "contact"
    template_name = "contact/list_view.html"
    context_object_name = "contacts"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            print("a")
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
        return queryset.order_by("name")

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
        context.update(more_context)
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
