from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
import uuid
from . import models as customerModels, forms as customerForms
from misc import models as miscModels
from plan import models as planModels

from tabernacle_customer_success import constants


class CustomerCreateView(View):
    template_name = "customer/create_view.html"
    title = "Customer Information"
    active_tab = "customer"

    def get(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm()

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_info_form": customer_info_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm(request.POST, request.FILES)

        if customer_info_form.is_valid():
            customer_info_object = customer_info_form.save()
            return redirect(
                reverse(
                    "customer:select-plan",
                    kwargs={"customer_id": customer_info_object.uuid},
                )
            )

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_info_form": customer_info_form,
        }
        return render(request, self.template_name, context)


class CustomerSelectPlanView(View):
    template_name = "customer/select_plan.html"
    title = "Select Plan"
    active_tab = "customer"

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get("customer_id")

        customer_plan_form = customerForms.CustomerPlanForm()
        plan_options_form = customerForms.PlanOptionsForm()

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_plan_form": customer_plan_form,
            "plan_options_form": plan_options_form,
            "customer_id": customer_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get("customer_id")

        plan_options_form = customerForms.PlanOptionsForm(request.POST)

        if plan_options_form.is_valid():

            plan_type = plan_options_form.cleaned_data["plan_type"]
            member_size = plan_options_form.cleaned_data["member_size"]
            duration = plan_options_form.cleaned_data["duration"]

            subscription_plan = planModels.SubscriptionPlan.objects.get(
                plan_type=plan_type, member_size=member_size
            )
            customerModels.CustomerPlan.objects.create(
                customer_id=customer_id,
                subscription_plan=subscription_plan,
                duration_in_months=duration,
            )
            request.session["selected_subscription_plan"] = str(subscription_plan.uuid)
            return redirect(reverse("customer:user-create",kwargs={'customer_id': customer_id}))

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "plan_options_form": plan_options_form,
            "subscription_plan": subscription_plan,
        }
        return render(request, self.template_name, context)


def load_states(request):
    country_id = request.GET.get("country_id")
    states = miscModels.State.objects.filter(country_id=country_id).order_by("name")
    return render(request, "customer/state_dropdown_list.html", {"states": states})


class CustomerListView(ListView):
    model = customerModels.CustomerInfo
    template_name = "customer/list_view.html"
    title = "Customer List"
    active_tab = "customer"
    context_object_name = "customers"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            print("a")
            queryset = queryset.filter(
                (
                    Q(legal_name__istartswith=search_query)
                    | Q(legal_name__icontains=" " + search_query)
                )
            )
        return queryset.order_by("legal_name")

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


class CustomerEditView(View):
    template_name = "customer/edit_view.html"
    title = "Edit Customer"
    active_tab = "customer"

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get("customer_id")
        customer_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_info_form = customerForms.CustomerInfoForm(instance=customer_object)

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_info_form": customer_info_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get("customer_id")
        customer_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_info_form = customerForms.CustomerInfoForm(
            request.POST, request.FILES, instance=customer_object
        )

        if customer_info_form.is_valid():
            customer_info_form.save()
            return redirect(reverse("customer:list"))

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_info_form": customer_info_form,
        }
        return render(request, self.template_name, context)


class UserCreateView(View):
    model = customerModels.CustomerUser
    template_name = "customer/form_user.html"
    title = "User Information"
    active_tab = "customer"

    def get(self, request, *args, **kwargs):
        customer_user_form = customerForms.CustomerUserForm()
        customer_userpermission_form = customerForms.UserAppPermissionsForm()
        if "selected_subscription_plan" in request.session:
            subscription_plan = planModels.SubscriptionPlan.objects.get(
                uuid=request.session["selected_subscription_plan"]
            )
            plan_type = subscription_plan.plan_type
            request.session.pop("selected_subscription_plan", None)
        else:
            subscription_plan = None
            plan_type = None
        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_user_form": customer_user_form,
            "customer_userpermission_form": customer_userpermission_form,
            "subscription_plan": subscription_plan,
            "plan_type": plan_type,
            "selected_modules": [],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get("customer_id")
        customer_info_object = get_object_or_404(customerModels.CustomerInfo, uuid=customer_id)
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        customer_userpermission_form = customerForms.UserAppPermissionsForm(request.POST)

        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save(commit=False)
            customer_user_object.customer = customer_info_object
            customer_user_object.save()
            customer_user = customerModels.CustomerUser.objects.get(uuid=uuid)
            selected_module = request.POST.getlist("modules")
            selected_module = selected_module[0] if selected_module else None
            new_user_app_permission = customerForms.UserAppPermissionsForm(
            user=customer_user,
            module="some_module",
            access_role="some_role"
            )
            new_user_app_permission.save()
            return redirect(
                reverse(
                    "customer:list"
                )
            )

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "customer_user_form": customer_user_form,
            "selected_module": selected_module,
            "customer_userpermission_form": customer_userpermission_form,
        }
        return render(request, self.template_name, context)