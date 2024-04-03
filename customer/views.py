# Dango Imports
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Project Imports
from . import models as customerModels, forms as customerForms
from prospect import models as prospectModels, forms as prospectForms
from plan import models as planModels
from django.contrib import messages

from tabernacle_customer_success import constants


class CustomerOnboardingView(View):
    template_name = 'customer/onboard_view.html'
    title = 'Onboarding'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_profile_form = customerForms.CustomerProfileForm()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_profile_form': customer_profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_profile_form = customerForms.CustomerProfileForm(
            request.POST, request.FILES
        )
        if customer_profile_form.is_valid():
            form_data = customer_profile_form.cleaned_data
            request.session['customer_profile_form_data'] = form_data
            customer_info_object = customer_profile_form.save()
            return redirect(
                reverse(
                    'customer:select-plan',
                    kwargs={'customer_id': customer_info_object.uuid},
                )
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_profile_form': customer_profile_form,
            
        }
        return render(request, self.template_name, context)


class CustomerSelectPlanView(View):
    template_name = 'customer/select_plan.html'
    title = 'Select Plan'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        form_data = request.session.get('customer_profile_form_data', {})
        customer_plan_form = customerForms.CustomerPlanForm(initial=form_data)
        plan_options_form = customerForms.SubscriptionPlanOptionsForm()
        if 'customer_profile_form_data' in request.session:
        # Remove the form data from the session to avoid using it again
            customer_profile_data = request.session.pop('customer_profile_form_data')

        # Set the form fields based on the stored data
        customer_plan_form = customerForms.CustomerPlanForm(initial=customer_profile_data)
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

        plan_options_form = customerForms.SubscriptionPlanOptionsForm(request.POST)

        if plan_options_form.is_valid():

            plan = request.POST.get('plan')
            duration = int(request.POST.get('duration'))
            payment_status = request.POST.get('payment_status')

            tariff = planModels.Tariff.objects.get(uuid=plan)

            try:
                subscribed_plan = customerModels.SubscribedPlan.objects.get(
                    customer_id=customer_id
                )
                subscribed_plan.subscription_plan = tariff
                subscribed_plan.duration = duration
                subscribed_plan.save()
            except:
                customerModels.SubscribedPlan.objects.create(
                    customer_id=customer_id,
                    subscription_plan=tariff,
                    duration=duration,
                )

            amount = int(tariff.amount) * duration
            payment_date = datetime.today()
            due_date = payment_date + relativedelta(months=duration)

            if payment_status == constants.PAID:
                payment_data = {
                    'customer_id': customer_id,
                    'amount': amount,
                    'payment_date': payment_date,
                    'due_date': due_date,
                }
                customerModels.PaymentHistory.objects.create(**payment_data)
            request.session['subscribed_plan'] = str(tariff.uuid)
            return redirect(
                reverse('customer:user-create', kwargs={'customer_id': customer_id})
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'plan_options_form': plan_options_form,
            'subscription_plan': tariff,
        }
        return render(request, self.template_name, context)


class CustomerListView(ListView):
    model = customerModels.Profile
    template_name = 'customer/list_view.html'
    title = 'Customer List'
    active_tab = 'customer'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                (
                    Q(legal_name__istartswith=search_query)
                    | Q(legal_name__icontains=' ' + search_query)
                )
            )
        queryset = queryset.order_by('legal_name')

        for query in queryset:
            try:
                last_payment = customerModels.PaymentHistory.objects.filter(customer_id=query.uuid).order_by('-created_at').first()
                query.due_date = last_payment.due_date
                
                days_difference = (query.due_date - datetime.now().date()).days
                if days_difference > 0 and days_difference < 30:
                    query.payment_status = constants.DUE
                elif days_difference < 0:
                    query.payment_status = constants.OVERDUE
                else:
                    query.payment_status = constants.PAID

                query.days_difference = abs(days_difference)
            except:
                try:
                    if query.customer_plan.duration == 0:
                        query.due_date = query.created_at.date() + timedelta(days=constants.TRIAL_DURATION)
                        query.payment_status = constants.EXPIRY
                        query.days_difference = (query.due_date - datetime.now().date()).days
                except:
                    query.payment_status = constants.PENDING

                
        return queryset

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
    title = 'Edit Customer Details'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_object = get_object_or_404(customerModels.Profile, uuid=customer_id)
        customer_profile_form = customerForms.CustomerProfileForm(instance=customer_object)

        prospect_object = get_object_or_404(prospectModels.Profile, uuid=customer_object.prospect_id)
        prospect_profile_form = prospectForms.ProspectProfileForm(instance=prospect_object)

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_profile_form': customer_profile_form,
            'prospect_profile_form': prospect_profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        customer_object = get_object_or_404(customerModels.Profile, uuid=customer_id)
        customer_profile_form = customerForms.CustomerProfileForm(
            request.POST, request.FILES, instance=customer_object
        )

        prospect_object = get_object_or_404(prospectModels.Profile, uuid=customer_object.prospect_id)
        prospect_profile_form = prospectForms.ProspectProfileForm(request.POST, instance=prospect_object)

        if customer_profile_form.is_valid() and prospect_profile_form.is_valid():
            customer_object = customer_profile_form.save()
            prospect_object = prospect_profile_form.save(commit=False)
            prospect_object.name = customer_object.legal_name
            prospect_object.save()
            return redirect(reverse('customer:list'))
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_profile_form': customer_profile_form,
        }
        return render(request, self.template_name, context)


class UserCreateView(View):
    model = customerModels.User
    template_name = 'customer/admin_user.html'
    title = 'User Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get_context(self):
        customer_id = self.kwargs.get('customer_id')
        customer_user_form = customerForms.CustomerUserForm(
            initial={'customer': customer_id}
        )
        return {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_id': customer_id,
            'customer_user_form': customer_user_form,
            'go_back_url': reverse(
                'customer:select-plan', kwargs={'customer_id': customer_id}
            ),
        }

    def get(self, request, *args, **kwargs):

        context = self.get_context()
        if 'subscribed_plan' in request.session:
            subscribed_plan = request.session['subscribed_plan']

            tariff = planModels.Tariff.objects.get(uuid=subscribed_plan)

            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                initial=[
                    {
                        'module': module,
                        'has_access': True,
                        'access_role': constants.VIEWER,
                    }
                    for module in tariff.modules
                ]
            )

            more_context = {
                'user_app_permissions_formset': user_app_permissions_formset,
            }
            context.update(more_context)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)

        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save()

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

            action = request.POST.get('action', None)

            if action == 'add_more_user':
                return redirect(
                    reverse(
                        'customer:user-add',
                        kwargs={'customer_id': customer_user_object.customer_id},
                    )
                )
            elif action == 'done':
                request.session.pop('subscribed_plan', None)
                return redirect(reverse('customer:list'))

        context = self.get_context()

        return render(request, self.template_name, context)


class AnotherUserCreateView(View):
    model = customerModels.User
    template_name = 'customer/assign_user_form.html'
    title = 'User Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_user_form = customerForms.CustomerUserForm(
            initial={'customer': customer_id}
        )

        if 'subscribed_plan' in request.session:
            subscribed_plan = request.session['subscribed_plan']

            tariff = planModels.Tariff.objects.get(uuid=subscribed_plan)

            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                initial=[
                    {
                        'module': module,
                    }
                    for module in tariff.modules
                ]
            )

        customer_id = self.kwargs.get('customer_id')
        users = customerModels.User.objects.filter(customer_id=customer_id)
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
            'users': users,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)

        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save()

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

            action = request.POST.get('action', None)

            if action == 'add_more_user':
                return redirect(
                    reverse(
                        'customer:user-add',
                        kwargs={'customer_id': customer_user_object.customer_id},
                    )
                )
            elif action == 'done':
                request.session.pop('subscribed_plan', None)
                return redirect(reverse('customer:list'))

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_user_form': customer_user_form,
            'user_app_permissions_formset': user_app_permissions_formset,
        }

        return render(request, self.template_name, context)
