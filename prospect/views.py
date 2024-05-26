import calendar
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from prospect import models as prospectModels, forms as prospectForms
from prospect.utils import Calendar
from tabernacle_customer_success import constants
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from .filters import ProfileFilter
from django.db.models import Q
from customer import models as customerModels

from datetime import date, timedelta
from django.db.models import Max

@method_decorator(login_required, name='dispatch')
class ProspectDashboardView(View):
    template_name = 'prospect/overview_view.html'
    title = 'Overview'
    active_tab = 'prospect'

    def _get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split("-"))
            return date(year, month, day=1)
        return datetime.datetime.today()


    def _prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
        return month


    def _next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = "month=" + str(next_month.year) + "-" + str(next_month.month)
        return month
    def get(self, request, *args, **kwargs):
        stats = {}
        stats['prospects'] = prospectModels.Profile.objects.exclude(status__in=[constants.TRIAL, constants.ACCEPTED, constants.REJECTED]).count()
        stats['opportunities'] = prospectModels.Profile.objects.filter(status=constants.TRIAL).count()
        stats['customers'] = prospectModels.Profile.objects.filter(status=constants.ACCEPTED).count()
        stats['lost_prospects'] = prospectModels.Profile.objects.filter(status=constants.REJECTED).count()


        firstweekday = 6  # sunday as the first weekday
        d = self._get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month, firstweekday)
        html_cal = cal.formatmonth(withyear=True)
        today = datetime.datetime.today()
        
        prospects_ids = prospectModels.Profile.objects.filter(status=constants.MEETING_SCHEDULED).distinct('uuid').values_list('uuid', flat=True)
        status_history = prospectModels.StatusHistory.objects.filter(
            date__month=today.month,
            date__year=today.year,
            prospect_id__in = prospects_ids,
            status=constants.MEETING_SCHEDULED
        ).order_by('prospect', 'created_at')
        latest_records = status_history.values('prospect').annotate(
            latest_date=Max('created_at')
        )

        latest_status_history = prospectModels.StatusHistory.objects.filter(
            date__month=today.month,
            date__year=today.year,
            status=constants.MEETING_SCHEDULED,
            prospect__in=latest_records.values_list('prospect', flat=True),
            created_at__in=latest_records.values_list('latest_date', flat=True)
        )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'stats': stats,
            'calendar': html_cal,
            'prev_month': self._prev_month(d),
            'current_month': d,
            'next_month': self._next_month(d),
            'today': today,
            'weekdays': cal.formatweekheader(),
            'month_events': latest_status_history
        }
        return render(request, self.template_name, context)



@method_decorator(login_required, name='dispatch')
class ProspectListView(ListView):
    model = prospectModels.Profile
    context_object_name = 'prospects'
    template_name = 'prospect/list_view.html'
    filterset_class = ProfileFilter
    title="Prospect List"
    active_tab="prospect"


    def search_query(self, queryset):
        search_query = self.request.GET.get('search')
        sort = self.request.GET.get("sort", "")
        status = self.request.GET.getlist("status")
        print("Sort:", sort)
        if search_query:
            queryset = queryset.filter(
                Q(name__istartswith=search_query) |
                Q(name__icontains=' ' + search_query)
            )
        if status:
            filter_form = self.filterset_class(self.request.GET, queryset=queryset)
            queryset = filter_form.qs 

        if sort:
            sort_field = constants.PROSPECT_SORT_CHOICES.get(sort, '')
            if sort_field:
                queryset = queryset.order_by(sort_field)
        
        return queryset
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.search_query(queryset)

        for query in queryset:
            status_history = prospectModels.StatusHistory.objects.filter(prospect_id=query.uuid).order_by('-created_at')
            if status_history.exists():
                query.status_history = status_history.first()
                if query.status_history.status == constants.TRIAL:
                    query.expiry_date = query.status_history.date + timedelta(days=14)
                    query.expiry_days = (query.expiry_date - timezone.now()).days
        return queryset

    def get_paginate_by(self, queryset):
        page_limit = self.request.GET.get('page_limit', constants.PAGINATION_LIMIT)
        if page_limit == 'all':
            page_limit = len(queryset)
        return self.request.GET.get('paginate_by', page_limit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_form = ProfileFilter(self.request.GET, queryset=self.get_queryset())
        context.update({
            "title": self.title,
            "active_tab": self.active_tab,
            "sort_options":constants.PROSPECT_SORT_CHOICES,
            "prospect_filter": filter_form,
            "status_list": self.request.GET.getlist("status"),
        })
        return context


@method_decorator(login_required, name='dispatch')
class ProspectCreateView(View):
    template_name = 'prospect/create_view.html'
    title = 'New Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(
            prefix='prospect', initial={'manager': request.user}
        )

        PointOfContactFormSet = formset_factory(
            prospectForms.PointOfContactForm,
            min_num=1,
            validate_min=True,
            extra=1,
            can_delete=True,
        )
        poc_formset = PointOfContactFormSet()

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_form = prospectForms.ProspectProfileForm(
            request.POST, prefix='prospect'
        )
        PointOfContactFormSet = formset_factory(
            prospectForms.PointOfContactForm, extra=2
        )
        poc_formset = PointOfContactFormSet(request.POST)

        try:
            if prospect_form.is_valid() and poc_formset.is_valid():
                prospect_object = prospect_form.save()
                for form in poc_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        point_of_contact_info = form.save(commit=False)
                        point_of_contact_info.prospect = prospect_object
                        point_of_contact_info.save()
                messages.success(request, 'Prospect has been successfully created')
                return redirect('prospect:list')
        except Exception as e:
            messages.error(request, 'Unsuccessful, try again')

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'poc_formset': poc_formset,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ProspectEditView(View):
    template_name = 'prospect/edit_view.html'
    title = 'Edit Prospect'
    active_tab = 'prospect'

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(
            instance=prospect, prefix='prospect'
        )

        has_customer = True if customerModels.Profile.objects.filter(prospect=prospect).exists() else False

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
            'has_customer': has_customer
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect_instance = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
        prospect_form = prospectForms.ProspectProfileForm(
            request.POST, instance=prospect_instance, prefix='prospect'
        )

        if prospect_form.is_valid():
            prospect_form.save()
            messages.success(
                request, 'Prospect information has been successfully updated'
            )
            return redirect('prospect:list')
        else:
            messages.error(
                request, 'Unsuccessful! Please check the form and try again.'
            )

        context = {
            'title': self.title,
            'active_tab': self.active_tab,
            'prospect_form': prospect_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UpdatePointOfContactView(View):
    template_name = 'prospect/edit_poc.html'
    title = 'Edit Point of Contact'
    PointOfContactFormSet = modelformset_factory(
        prospectModels.PointOfContact,
        form=prospectForms.PointOfContactForm,
        extra=2,
        exclude=(),
        min_num=0,
        max_num=2,
        can_delete=True,
    )

    def get(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)
                
        poc_formset = self.PointOfContactFormSet(
            queryset=prospect.prospect_poc.all(),
        )

        context = {
            'title': self.title,
            'poc_formset': poc_formset,
            'prospect': prospect,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        prospect_id = kwargs.get('prospect_id')
        prospect = get_object_or_404(prospectModels.Profile, uuid=prospect_id)

        poc_formset = self.PointOfContactFormSet(
            request.POST, queryset=prospect.prospect_poc.all()
        )

        if poc_formset.is_valid():
            for form in poc_formset:
                if form.cleaned_data:
                    if form.is_empty() and form.instance.pk:
                        form.instance.delete()
                    else:
                        point_of_contact_info = form.save(commit=False)
                        point_of_contact_info.prospect = prospect
                        point_of_contact_info.save()
            messages.success(request, 'Point of Contact updated successfully')
            return redirect('prospect:list')
        else:
            messages.error(request, 'Unable to update Point of Contact. Try again.')

        context = {
            'title': self.title,
            'poc_formset': poc_formset,
            'prospect': prospect,
            'active_tab': 'prospect',
        }
        return render(request, self.template_name, context)
