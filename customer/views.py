# Dango Imports
from django.db.models import Q
from django.forms import modelformset_factory,formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal

from uuid import UUID
# Project Imports
from . import models as customerModels, forms as customerForms
from prospect import models as prospectModels, forms as prospectForms
from plan import models as planModels
from django.contrib import messages
from misc import models as miscModels
from tabernacle_customer_success import constants, helper


@method_decorator(login_required, name='dispatch')
class CustomerOnboardingView(View):
    template_name = 'customer/onboard_customer_view.html'
    title = 'Onboarding'
    active_tab = 'customer'
    
    def get_context_data(self):
        customer_id = self.kwargs.get('customer_id')
        customer_profile = customerModels.Profile.objects.get(uuid=customer_id)
        context = {
            'title': f'{self.title}: {customer_profile.prospect.name}',
            'active_tab': self.active_tab,
            'customer': customer_profile,
        }
        return context
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        customer_profile_form = customerForms.CustomerProfileForm(instance=context['customer'])
        more_context = {
            'customer_profile_form': customer_profile_form
        }
        context.update(more_context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        customer_profile_form = customerForms.CustomerProfileForm(request.POST, request.FILES, instance=context['customer'])

        if customer_profile_form.is_valid():
            customer_info_object = customer_profile_form.save(commit=False)
            customer_info_object.manager = request.user
            customer_info_object.save()
            
            profile_uuid = customer_info_object.uuid
            request.session['customer_profile_uuid'] = str(profile_uuid)
            return redirect(
                reverse(
                    'customer:onboard-select-plan',
                    kwargs={'customer_id': customer_info_object.uuid},
                )
            )
            
        more_context = {
            'customer_profile_form': customer_profile_form
        }
        context.update(more_context)

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class OnboardingPlanView(View):
    template_name = 'customer/onboard_select_plan.html'
    title = 'Select Plan'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer_profile_uuid_str = request.session.get('customer_profile_uuid')
       
        customer_plan_form = customerForms.CustomerPlanForm()
        plan_options_form = customerForms.SubscriptionPlanOptionsForm()
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_id': customer_id,
        }

        if customer_profile_uuid_str:
            try:
                customer_profile_uuid = UUID(customer_profile_uuid_str)
                profile = customerModels.Profile.objects.get(uuid=customer_profile_uuid)
                
                profile2=customerModels.SubscribedPlan.objects.get(customer=profile)
                
                customer_plan_form = customerForms.CustomerPlanForm(instance=profile2)
                
                plan_options_form = customerForms.SubscriptionPlanOptionsForm(initial={
                        'plan': profile2.subscription_plan,
                        'duration': profile2.duration,
                        'payment_status': profile2.payment_status
                    })
            except:
               pass


        context['customer_plan_form'] = customer_plan_form
        context['plan_options_form'] = plan_options_form

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')

        plan_options_form = customerForms.SubscriptionPlanOptionsForm(request.POST)

        if plan_options_form.is_valid():

            plan = request.POST.get('plan')
            is_yearly = request.POST.get('is_yearly')
            discount = 0 if request.POST.get('discount') == '' else request.POST.get('discount')

            duration = 12 if is_yearly else 1
            payment_status = request.POST.get('payment_status')
            customer_profile_uuid=request.POST.get('customer_id')
            tariff = planModels.Tariff.objects.get(uuid=plan)

            try:
                subscribed_plan = customerModels.SubscribedPlan.objects.get(
                    customer_id=customer_id
                )
                subscribed_plan.subscription_plan = tariff
                subscribed_plan.duration = duration
                subscribed_plan.save()
                
            except:
                subscribed_plan = customerModels.SubscribedPlan.objects.create(
                    customer_id=customer_id,
                    subscription_plan=tariff,
                    duration=duration,
                )

            request.session['subscribed_plan_id'] = str(subscribed_plan.subscription_plan.uuid)

            if duration == 12:
                amount = helper.get_discounted_amount((tariff.amount * duration), 15) - Decimal(discount)
            else:
                amount = tariff.amount - Decimal(discount)

            payment_date = datetime.today()
            due_date = payment_date + relativedelta(months=duration)

            payment_data = {
                'customer_id': customer_id,
                'amount': amount,
                'payment_date': payment_date,
                'due_date': due_date,
                'payment_status': payment_status,
                'discount': discount,
            }
            customerModels.PaymentHistory.objects.create(**payment_data)
            customer_profile_uuid = customer_id
            request.session['customer_profile_uuid'] = str(customer_profile_uuid)
            return redirect(
                reverse('customer:onboard-user-create', kwargs={'customer_id': customer_id})
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'plan_options_form': plan_options_form,
            'subscription_plan': tariff,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CustomerListView(ListView):
    model = customerModels.Profile
    template_name = 'customer/list_view.html'
    title = 'Customer List'
    active_tab = 'customer'
    context_object_name = 'customers'

    def get_queryset(self):
        request=self.request
        if 'customer_profile_uuid' in request.session:
            del request.session['customer_profile_uuid']
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                (
                    Q(legal_name__istartswith=search_query)
                    | Q(legal_name__icontains=' ' + search_query)
                )
            )
        queryset = queryset.order_by('official_name')

        for query in queryset:
            try:
                last_payment = customerModels.PaymentHistory.objects.filter(customer_id=query.uuid).order_by('-created_at').first()
                query.due_date = last_payment.due_date
                days_difference = (query.due_date - timezone.now()).days
                
                if days_difference > 0 and days_difference < 30:
                    query.payment_status = constants.DUE
                elif days_difference < 0:
                    query.payment_status = constants.OVERDUE
                else:
                    query.payment_status = last_payment.payment_status
                
                query.amount = last_payment.amount
            
                if query.due_date:
                    if query.due_date > timezone.now():
                        query.days_difference = (query.due_date - timezone.now()).days
                    else:
                        query.days_difference = (timezone.now() - query.due_date).days
            except:
                pass
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


@method_decorator(login_required, name='dispatch')
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
            prospect_object.name = customer_object.official_name
            prospect_object.save()
            return redirect(reverse('customer:list'))
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_profile_form': customer_profile_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class OnboardingUserView(View):
    model = customerModels.User
    template_name = 'customer/onboard_user_view.html'
    title = 'Collaborator Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get_context(self):
        customer_id = self.kwargs.get('customer_id')
        customer_user_form = customerForms.CustomerUserForm(
            initial={'customer': customer_id}
        )
        users = customerModels.User.objects.filter(customer_id=customer_id)
        return {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_id': customer_id,
            'customer_user_form': customer_user_form,
            'users': users,
            'go_back_url': reverse(
                'customer:onboard-select-plan', kwargs={'customer_id': customer_id}
            ),
            'is_next_user': True if 'next' in self.request.get_full_path() else False
        }

    def get(self, request, *args, **kwargs):
        
        context = self.get_context()
        if 'subscribed_plan_id' in request.session:
            subscribed_plan_id = request.session['subscribed_plan_id']

            tariff = planModels.Tariff.objects.get(uuid=subscribed_plan_id)
            
            modules = miscModels.AppModule.objects.filter(name__in=tariff.modules).order_by('precedance')

            if context['is_next_user']:
                user_app_permissions_formset = self.UserAppPermissionsFormSet(
                    initial=[{
                        'module': module,
                        'module_name': module.name,
                        } for module in modules])
            else:
                user_app_permissions_formset = self.UserAppPermissionsFormSet(
                    initial=[{
                        'module': module,
                        'module_name': module.name,
                        'has_access': True,
                        'access_role': constants.EDITOR,
                    } for module in modules])
            
            for form in user_app_permissions_formset:
                form.permissions = form.initial['module'].permissions

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

                    if user_app_permissions_form.cleaned_data['has_access'] == 'True' and len(user_app_permissions_form_object.module.permissions) == 0:
                            user_app_permissions_form_object.access_role = constants.ALL_ACCESS
                    elif user_app_permissions_form.cleaned_data['has_access'] == 'True' and len(user_app_permissions_form_object.module.permissions) > 0:
                        user_app_permissions_form_object.access_role = user_app_permissions_form.cleaned_data['access_role']
                    else:
                        continue
                    user_app_permissions_form_object.save()

            action = request.POST.get('action', None)

            if action == 'add_more_user':
                return redirect(
                    reverse(
                        'customer:onboard-user-create-next',
                        kwargs={'customer_id': customer_user_object.customer_id},
                    )
                )
            elif action == 'done':
                request.session.pop('subscribed_plan_id')
                return redirect(reverse('customer:list'))

        context = self.get_context()

        return render(request, self.template_name, context)
@method_decorator(login_required, name='dispatch')
class AddCollaboratorView(View):
    model = customerModels.User
    template_name = 'customer/edit_collaborator.html'
    title = 'Collaborator Information'
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
                'customer:users', kwargs={'customer_id': customer_id}
            ),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        subscribed_plan = customerModels.SubscribedPlan.objects.get(customer=context['customer_id'])
        first_customers = customerModels.User.objects.filter(customer=context['customer_id']).order_by('created_at').first()
        tariff = planModels.Tariff.objects.get(uuid=subscribed_plan.subscription_plan.uuid)
        
        modules = miscModels.AppModule.objects.filter(name__in=tariff.modules).order_by('precedance')
        is_next_user = True
        
        if is_next_user:
            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                    initial=[{
                        'module': module,
                        'module_name': module.name,
                        } for module in modules])
            is_next_user = False
        else:
            initial_data = [{
                'module': module,
                'module_name': module.name,
                'has_access': True,
                'access_role': constants.EDITOR,
            } for module in modules]
            user_app_permissions_formset = self.UserAppPermissionsFormSet(initial=initial_data)
        
        for form in user_app_permissions_formset:
            form.permissions = form.initial['module'].permissions

        more_context = {
            'user_app_permissions_formset': user_app_permissions_formset,
            'is_next_user': is_next_user
        }
        context.update(more_context)

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = self.get_context()

        customer_id = self.kwargs.get('customer_id')
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)
        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save()
            if user_app_permissions_formset.is_valid():
                for user_app_permissions_form in user_app_permissions_formset:
                    if user_app_permissions_form.cleaned_data.get('has_access') == 'True':
                        module = user_app_permissions_form.cleaned_data.get('module')
                        try:
                            user_app_permissions_object = customerModels.UserAppPermissions.objects.get(
                                user=customer_user_object,
                                module=module
                            )
                        except customerModels.UserAppPermissions.DoesNotExist:
                            user_app_permissions_object = user_app_permissions_form.save(commit=False)
                            user_app_permissions_object.user = customer_user_object

                        if len(module.permissions) == 0:
                            user_app_permissions_object.access_role = constants.ALL_ACCESS
                        else:
                            user_app_permissions_object.access_role = user_app_permissions_form.cleaned_data.get('access_role')
                        
                        user_app_permissions_object.save()
                    else:
                        module = user_app_permissions_form.cleaned_data.get('module')
                        try:
                            user_app_permissions_object = customerModels.UserAppPermissions.objects.get(
                                user=customer_user_object,
                                module=module
                            )
                            user_app_permissions_object.delete()
                        except customerModels.UserAppPermissions.DoesNotExist:
                            pass
        else:
            return render(request, self.template_name, context)
        return redirect(reverse('customer:users', kwargs={'customer_id': customer_id}))

@method_decorator(login_required, name='dispatch')
class EditCollaboratorView(View):
    model = customerModels.User
    template_name = 'customer/edit_collaborator.html'
    title = 'Collaborator Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get_context(self):
        customer_id = self.kwargs.get('customer_id')
        colab_id = self.kwargs.get('collaborator_id')
        collaborator = customerModels.User.objects.get(uuid=colab_id)
        customer_user_form = customerForms.CustomerUserForm(instance = collaborator,
            initial={'customer': customer_id}
        )
        return {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_id': customer_id,
            'colab_id': colab_id,
            'customer_user_form': customer_user_form,
            'go_back_url': reverse(
                'customer:users', kwargs={'customer_id': customer_id}
            ),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        subscribed_plan = customerModels.SubscribedPlan.objects.get(customer=context['customer_id'])
        first_customers = customerModels.User.objects.filter(customer=context['customer_id']).order_by('created_at').first()
        tariff = planModels.Tariff.objects.get(uuid=subscribed_plan.subscription_plan.uuid)
        
        modules = miscModels.AppModule.objects.filter(name__in=tariff.modules).order_by('precedance')
        collaborator = customerModels.UserAppPermissions.objects.filter(user__uuid=context['colab_id'])
        is_next_user = True
        
        if context['colab_id'] != first_customers.uuid:
            initial_data = []
            for module in modules:
                data = collaborator.filter(module=module).first()
                if data:
                    initial_data.append({
                        'module': module,
                        'module_name': module.name,
                        'has_access': True,
                        'access_role': data.access_role
                    })
                else:
                    initial_data.append({
                        'module': module,
                        'module_name': module.name,
                        'has_access': False,
                        'access_role': None
                    })
            user_app_permissions_formset = self.UserAppPermissionsFormSet(initial=initial_data)
            is_next_user = False

        else:
            initial_data = [{
                'module': module,
                'module_name': module.name,
                'has_access': True,
                'access_role': constants.EDITOR,
            } for module in modules]
            user_app_permissions_formset = self.UserAppPermissionsFormSet(initial=initial_data)
        
        for form in user_app_permissions_formset:
            form.permissions = form.initial['module'].permissions

        more_context = {
            'user_app_permissions_formset': user_app_permissions_formset,
            'is_next_user': is_next_user
        }
        context.update(more_context)

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = self.get_context()

        colab_id = self.kwargs.get('collaborator_id')
        collaborator = customerModels.User.objects.get(uuid=colab_id)
        customer_user_form = customerForms.CustomerUserForm(request.POST, instance=collaborator )
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)
        if customer_user_form.is_valid():
            customer_user_object = customer_user_form.save()
            if user_app_permissions_formset.is_valid():
                for user_app_permissions_form in user_app_permissions_formset:
                    if user_app_permissions_form.cleaned_data.get('has_access') == 'True':
                        module = user_app_permissions_form.cleaned_data.get('module')
                        try:
                            user_app_permissions_object = customerModels.UserAppPermissions.objects.get(
                                user=customer_user_object,
                                module=module
                            )
                        except customerModels.UserAppPermissions.DoesNotExist:
                            user_app_permissions_object = user_app_permissions_form.save(commit=False)
                            user_app_permissions_object.user = customer_user_object

                        if len(module.permissions) == 0:
                            user_app_permissions_object.access_role = constants.ALL_ACCESS
                        else:
                            user_app_permissions_object.access_role = user_app_permissions_form.cleaned_data.get('access_role')
                        
                        user_app_permissions_object.save()
                    else:
                        module = user_app_permissions_form.cleaned_data.get('module')
                        try:
                            user_app_permissions_object = customerModels.UserAppPermissions.objects.get(
                                user=customer_user_object,
                                module=module
                            )
                            user_app_permissions_object.delete()
                        except customerModels.UserAppPermissions.DoesNotExist:
                            pass
        else:
            return render(request, self.template_name, context)
        return redirect(reverse('customer:users', kwargs={'customer_id': collaborator.customer.uuid}))



@method_decorator(login_required, name='dispatch')
class CustomerUsersView(ListView):
    model = customerModels.User
    template_name = 'customer/users_view.html'
    title = 'Collaborators'
    active_tab = 'customer'
    context_object_name = 'customer_users'

    def search_query(self, queryset):
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(full_name__istartswith=search_query) |
                Q(full_name__icontains=' ' + search_query)
            )
        return queryset

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        customer = get_object_or_404(customerModels.Profile, uuid=customer_id)
        queryset = customerModels.User.objects.filter(customer=customer).order_by('created_at')
        queryset = self.search_query(queryset)
        for user in queryset:
            user.app_permissions = customerModels.UserAppPermissions.objects.filter(user=user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs.get('customer_id')
        customer = get_object_or_404(customerModels.Profile, uuid=customer_id)
        context['title'] = f'{self.title} for {customer.official_name}'
        context['active_tab'] = self.active_tab
        context['customer_id'] = customer_id
        return context

@method_decorator(login_required, name='dispatch')
class UserCreateView(View):
    model = customerModels.User
    template_name = 'customer/user_create_view.html'
    title = 'Create User'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer= get_object_or_404(customerModels.Profile, uuid=customer_id)
        customer_users = get_object_or_404(customerModels.User, customer=customer)
        context = {
            'title': f'{self.title} for {customer.official_name}',
            'active_tab': self.active_tab,
            'customer_users': customer_users,
            'customer_id': customer_id
        }
        return render(request, self.template_name, context)




@method_decorator(login_required, name='dispatch')
class ChangePlanView(View):
    model = customerModels.User
    template_name = 'customer/change_plan_view.html'
    title = 'Change Plan'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer= get_object_or_404(customerModels.Profile, uuid=customer_id)
        context = {
            'title': f'{self.title} for {customer.official_name}',
            'active_tab': self.active_tab,
            'customer_id': customer_id
        }
        return render(request, self.template_name, context)
    


@method_decorator(login_required, name='dispatch')
class CalendarSample(View):
    model = customerModels.User
    template_name = 'customer/calendar_sample.html'
    title = 'Calendar Sample'
    active_tab = 'customer'

    def get(self, request, *args, **kwargs):
        context = {
            'title': self.title,
            'active_tab': self.active_tab,
        }
        return render(request, self.template_name, context)