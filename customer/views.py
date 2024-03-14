from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
import uuid
from . import models as customerModels, forms as customerForms
from misc import models as miscModels
from plan import models as planModels
from django.contrib import messages

from tabernacle_customer_success import constants
from django.forms import modelformset_factory, formset_factory


class CustomerOnboardingView(View):
    template_name = 'customer/onboard_view.html'
    title = 'Onboarding'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_info_form = customerForms.CustomerInfoForm(request.POST, request.FILES)

        if customer_info_form.is_valid():
            customer_info_object = customer_info_form.save()
            return redirect(
                reverse(
                    'customer:select-plan',
                    kwargs={'customer_id': customer_info_object.uuid},
                )
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form,
        }
        return render(request, self.template_name, context)


class CustomerSelectPlanView(View):
    template_name = 'customer/select_plan.html'
    title = 'Select Plan'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        customer_plan_form = customerForms.CustomerPlanForm()
        plan_options_form = customerForms.PlanOptionsForm()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_plan_form': customer_plan_form,
            'plan_options_form': plan_options_form,
            'customer_id': customer_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        plan_options_form = customerForms.PlanOptionsForm(request.POST)

        if plan_options_form.is_valid():

            plan_type = plan_options_form.cleaned_data['plan_type']
            member_size = plan_options_form.cleaned_data['member_size']
            duration = plan_options_form.cleaned_data['duration']

            subscription_plan = planModels.SubscriptionPlan.objects.get(
                plan_type=plan_type, member_size=member_size
            )
            customerModels.CustomerPlan.objects.create(
                customer_id=customer_id,
                subscription_plan=subscription_plan,
                duration_in_months=duration,
            )
            request.session['selected_subscription_plan'] = str(subscription_plan.uuid)
            return redirect(
                reverse('customer:user-create', kwargs={'customer_id': customer_id})
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'plan_options_form': plan_options_form,
            'subscription_plan': subscription_plan,
        }
        return render(request, self.template_name, context)


def load_states(request):
    country_id = request.GET.get('country_id')
    states = miscModels.State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'customer/state_dropdown_list.html', {'states': states})


class CustomerListView(ListView):
    model = customerModels.CustomerInfo
    template_name = 'customer/list_view.html'
    title = 'Customer List'
    active_tab = 'customer'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            print('a')
            queryset = queryset.filter(
                (
                    Q(legal_name__istartswith=search_query)
                    | Q(legal_name__icontains=' ' + search_query)
                )
            )
        return queryset.order_by('legal_name')

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        more_context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        context.update(more_context)
        return context


class CustomerEditView(View):
    template_name = 'customer/edit_view.html'
    title = 'Edit Customer'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_info_form = customerForms.CustomerInfoForm(instance=customer_object)

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_info_form = customerForms.CustomerInfoForm(
            request.POST, request.FILES, instance=customer_object
        )

        if customer_info_form.is_valid():
            customer_info_form.save()
            return redirect(reverse('customer:list'))

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_info_form': customer_info_form,
        }
        return render(request, self.template_name, context)


class UserCreateView(View):
    model = customerModels.CustomerUser
    template_name = 'customer/form_user.html'
    title = 'User Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get(self, request, *args, **kwargs):
        customer_user_form = customerForms.CustomerUserForm()
        customer_userpermission_form = customerForms.AddUserAppPermissionsForm()

        if 'selected_subscription_plan' in request.session:
            subscription_plan = planModels.SubscriptionPlan.objects.get(
                uuid=request.session['selected_subscription_plan']
            )

            plan_type = subscription_plan.plan_type
            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                initial=[
                    {
                        'module': module,
                        'has_access': True, #remove this for the other pages. default is false.
                        'access_role': constants.VIEWER,  #remove this for the other pages, where it's not selected by default.
                    }
                    for module in plan_type.modules
                ]
            )

        else:
            subscription_plan = None
            plan_type = None
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        customer_id = self.kwargs.get('customer_id')
        customer_info_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)

        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save(commit=False)
            customer_user_object.customer = customer_info_object
            customer_user_object.save()

            if user_app_permissions_formset.is_valid():
                for user_app_permissions_form in user_app_permissions_formset:
                    user_app_permissions_form_object = user_app_permissions_form.save(
                        commit=False
                    )
                    user_app_permissions_form_object.user = customer_user_object

                    if user_app_permissions_form.cleaned_data['has_access'] == 'True':
                        user_app_permissions_form_object.access_role = (
                            user_app_permissions_form.cleaned_data['access_role']
                        )
                    else:
                        user_app_permissions_form_object.access_role = None
                    user_app_permissions_form_object.save()
            
            messages.success(request, 'Employee Access Successfully Updated')
            next = request.POST.get('next', '')
            print(f"next: {next}, customer_id: {customer_id}")
            if next:
                if next == 'customer:user-add':
                    return redirect(reverse('customer:user-add', kwargs={'customer_id': customer_id}))
                elif next == 'customer:list':
                    return redirect(reverse('customer:list')) #redirect to next page (other users)

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
        }
        # request.session.pop('selected_subscription_plan', None)

        return render(request, self.template_name, context)

class AnotherUserCreateView(View):
    model = customerModels.CustomerUser
    template_name = 'customer/assign_user_form.html'
    title = 'User Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )
    # def get_queryset(self):
        

    def get(self, request, *args, **kwargs):
        customer_user_form = customerForms.CustomerUserForm()
        customer_userpermission_form = customerForms.AddUserAppPermissionsForm()

        if 'selected_subscription_plan' in request.session:
            subscription_plan = planModels.SubscriptionPlan.objects.get(
                uuid=request.session['selected_subscription_plan']
            )

            plan_type = subscription_plan.plan_type
            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                initial=[
                    {
                        'module': module,
                        # 'has_access': True, #remove this for the other pages. default is false.
                        # 'access_role': constants.VIEWER,  #remove this for the other pages, where it's not selected by default.
                    }
                    for module in plan_type.modules
                ]
            )

        else:
            subscription_plan = None
            plan_type = None
        customer_id = self.kwargs.get('customer_id')
        users = customerModels.CustomerUser.objects.filter(customer_id=customer_id)
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
            'users': users,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_info_object = get_object_or_404(
            customerModels.CustomerInfo, uuid=customer_id
        )
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)

        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save(commit=False)
            customer_user_object.customer = customer_info_object
            customer_user_object.save()

            if user_app_permissions_formset.is_valid():
                for user_app_permissions_form in user_app_permissions_formset:
                    user_app_permissions_form_object = user_app_permissions_form.save(
                        commit=False
                    )
                    user_app_permissions_form_object.user = customer_user_object

                    if user_app_permissions_form.cleaned_data['has_access'] == 'True':
                        user_app_permissions_form_object.access_role = (
                            user_app_permissions_form.cleaned_data['access_role']
                        )
                    else:
                        user_app_permissions_form_object.access_role = None
                    user_app_permissions_form_object.save()

            messages.success(request, 'Employee Access Successfully Updated')
            next = request.POST.get('next', '')
            print(f"next: {next}, customer_id: {customer_id}")
            if next:
                if next == 'customer:user-add':
                    return redirect(reverse('customer:user-add', kwargs={'customer_id': customer_id}))
                elif next == 'customer:list':
                    return redirect(reverse('customer:list')) #redirect to next page (other users)

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
        }
        # request.session.pop('selected_subscription_plan', None)

        return render(request, self.template_name, context)
