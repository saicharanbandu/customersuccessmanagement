# Dango Imports
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from .filters import CustomerFilter
from uuid import UUID

# Project Imports
from . import models as customerModels, forms as customerForms
from prospect import models as prospectModels, forms as prospectForms
from plan import models as planModels
from django.contrib import messages
from misc import models as miscModels
from tabernacle_customer_success import constants, helper


@method_decorator(login_required, name='dispatch')
class OnboardingCustomerView(View):
    template_name = 'customer/onboard/customer_view.html'
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
    template_name = 'customer/onboard/select_plan.html'
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
    filterset_class = CustomerFilter
    template_name = 'customer/customer/list_view.html'
    title = 'Customer List'
    active_tab = 'customer'
    context_object_name = 'customers'
    
    def search_query(self, queryset):
        
        search_query = self.request.GET.get('search')
        plan_status = self.request.GET.getlist("plan_status")
        
        if search_query:
            queryset = queryset.filter(
                Q(official_name__istartswith=search_query) |
                Q(official_name__icontains=' ' + search_query)
            )
        
        if plan_status:
            filter_form = self.filterset_class(self.request.GET, queryset=queryset)
            queryset = filter_form.qs
        
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        
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
        
        return self.search_query(queryset)

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = CustomerFilter(self.request.GET, queryset=self.get_queryset())
        more_context = {
            'title': self.title,
            'active_tab': self.active_tab,
            "sort_options": constants.customer_sort_options,
            "plan_filter": filter_form,
            "plan_status_list": self.request.GET.getlist("plan_status"),
        }
        context.update(more_context)
        return context

@method_decorator(login_required, name='dispatch')
class CustomerEditView(View):
    template_name = 'customer/customer/edit_view.html'
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
    template_name = 'customer/onboard/user_view.html'
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
class CustomerCollaboratorsView(ListView):
    model = customerModels.User
    template_name = 'customer/collaborator/list_view.html'
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
class AddCollaboratorView(View):
    model = customerModels.User
    template_name = 'customer/collaborator/add_view.html'
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
        tariff = planModels.Tariff.objects.get(uuid=subscribed_plan.subscription_plan.uuid)
        modules = miscModels.AppModule.objects.filter(name__in=tariff.modules).order_by('precedance')

        collaborators = customerModels.User.objects.filter(customer=context['customer_id'])

        if not collaborators.exists():
            is_admin = True
            user_app_permissions_formset = self.UserAppPermissionsFormSet(
                    initial=[{
                        'module': module,
                        'module_name': module.name,
                        } for module in modules])
        else:
            is_admin = False
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
            'is_admin': is_admin,
        }
        context.update(more_context)

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = self.get_context()

        customer_id = self.kwargs.get('customer_id')
        customer_user_form = customerForms.CustomerUserForm(request.POST)
        user_app_permissions_formset = self.UserAppPermissionsFormSet(request.POST)

        if not customer_user_form.is_valid():
            return render(request, self.template_name, context)
        
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
        return redirect(reverse('customer:users', kwargs={'customer_id': customer_id}))


@method_decorator(login_required, name='dispatch')
class EditCollaboratorView(View):
    model = customerModels.User
    template_name = 'customer/collaborator/edit_view.html'
    title = 'Collaborator Information'
    active_tab = 'customer'

    UserAppPermissionsFormSet = formset_factory(
        form=customerForms.AddUserAppPermissionsForm, extra=0
    )

    def get_context(self):
        customer_id = self.kwargs.get('customer_id')
        collaborator_id = self.kwargs.get('collaborator_id')
        collaborator = customerModels.User.objects.get(uuid=collaborator_id)
        customer_user_form = customerForms.CustomerUserForm(instance = collaborator,
            initial={'customer': customer_id}
        )
        return {
            'title': self.title,
            'active_tab': self.active_tab,
            'customer_id': customer_id,
            'collaborator_id': collaborator_id,
            'customer_user_form': customer_user_form,
            'go_back_url': reverse(
                'customer:users', kwargs={'customer_id': customer_id}
            ),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        subscribed_plan = customerModels.SubscribedPlan.objects.get(customer=context['customer_id'])
        first_collaborator = customerModels.User.objects.filter(customer=context['customer_id']).order_by('created_at').first()
        tariff = planModels.Tariff.objects.get(uuid=subscribed_plan.subscription_plan.uuid)
        
        modules = miscModels.AppModule.objects.filter(name__in=tariff.modules).order_by('precedance')
        collaborator = customerModels.UserAppPermissions.objects.filter(user__uuid=context['collaborator_id'])
        is_admin = True
        
        if context['collaborator_id'] != first_collaborator.uuid:
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
            is_admin = False

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
            'is_admin': is_admin
        }
        context.update(more_context)

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = self.get_context()

        collaborator_id = self.kwargs.get('collaborator_id')
        collaborator = customerModels.User.objects.get(uuid=collaborator_id)
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
    
class CustomerDashboardView(View):
    template_name = 'customer/overview_view.html'
    title = 'Customer Overview'
   
    def get(self, request, *args, **kwargs):
        
        context = {
            'title': self.title,
        }
        return render(request, self.template_name, context)
class PaymentView(View):
    template_name = "customer/payment.html"
    title = "Record Payment"
    active_tab = "payment"

    def get(self, request, customer_id, *args, **kwargs):
        customer = get_object_or_404(customerModels.Profile, uuid=customer_id)
        payment_form = customerForms.PaymentHistoryForm(initial={'created_by': request.user, 'payment_date': datetime.now()})

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "payment_form": payment_form,
            "customer": customer,
        }

        return render(request, self.template_name, context)

    def post(self, request, customer_id, *args, **kwargs):
        customer = get_object_or_404(customerModels.Profile, uuid=customer_id)
        payment_form = customerForms.PaymentHistoryForm(request.POST)

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.customer = customer  
            payment.created_by = request.user
            subscribed_plan = customer.customer_plan
            
            if not payment.due_date:  
                payment.due_date = datetime.now() + timedelta(days=subscribed_plan.duration*30)
            payment.save()
            return redirect(reverse("customer:payment_list", kwargs={"customer_id": customer.uuid}))

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "payment_form": payment_form,
            "customer": customer,
        }
        return render(request, self.template_name, context)
class PaymentListView(ListView):
    model = customerModels.PaymentHistory
    title = "Payment Directory"
    active_tab = "payment"
    template_name = "customer/payment_list.html"
    context_object_name = "payments"

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        payments = customerModels.PaymentHistory.objects.filter(customer_id=customer_id)
        return payments
    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get("page_limit", constants.PAGINATION_LIMIT)
        if page_limit == "all":
            page_limit = len(queryset)
        return self.request.GET.get("paginate_by", page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(customerModels.Profile, uuid=self.kwargs['customer_id'])
        context.update({
            "title": self.title,
            "active_tab": self.active_tab,
            "customer": customer,
        })
        return context
    
class PaymentEditView(View):
    title = "Edit Payment"
    active_tab = "payment"
    template_name = "customer/payment_edit.html"

    def get(self, request, payment_id, *args, **kwargs):
        payment = get_object_or_404(customerModels.PaymentHistory, uuid=payment_id)
        customer = get_object_or_404(customerModels.Profile, uuid=payment.customer_id)
        payment_form = customerForms.PaymentHistoryForm(instance=payment)
        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "payment_form": payment_form,
            "customer": customer,
            "payment": payment,
        }
        return render(request, self.template_name, context)

    def post(self, request, payment_id, *args, **kwargs):
        payment = get_object_or_404(customerModels.PaymentHistory, uuid=payment_id)
        customer = get_object_or_404(customerModels.Profile, uuid=payment.customer_id)
        payment_form = customerForms.PaymentHistoryForm(request.POST, instance=payment)

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.customer = customer
            payment.created_by = request.user
            subscribed_plan = customer.customer_plan
            
            if not payment.due_date:  
                payment.due_date = datetime.now() + timedelta(days=subscribed_plan.duration * 30)
            payment.save()
            return redirect(reverse("customer:payment_list", kwargs={"customer_id": customer.uuid}))

        context = {
            "title": self.title,
            "active_tab": self.active_tab,
            "payment_form": payment_form,
            "customer": customer,
            "payment": payment,
        }
        return render(request, self.template_name, context)