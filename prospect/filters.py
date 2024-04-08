# import django_filters
# from django import forms
# from tabernacle_customer_success import constants

# class ProspectFilter(django_filters.FilterSet):
#     date_range = django_filters.ChoiceFilter(
#         empty_label=None,
#         label='Date Range Type',
#         choices=constants.DATE_RANGE_FILTER_CHOICES,
#         method='filter_by_date_range_type',
#         widget=forms.RadioSelect(
#             attrs={'class': 'form-check-input filter-select'}))

#     start_date = django_filters.DateFilter(
#         label='Start Date',
#         method='filter_by_custom_date_range',
#         lookup_expr='range',
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         required=True)

#     end_date = django_filters.DateFilter(
#         label='End Date',
#         method='filter_by_custom_date_range',
#         lookup_expr='range',
#         widget=forms.DateInput(attrs={
#             'type': 'date',
#         }),
#         required=True)

#     status = django_filters.MultipleChoiceFilter(
#         label='Status',
#         method='filter_by_status',
#         choices=constants.PROSPECT_STATUS_CHOICES,
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'filter-select'}),
#     )
    
#     sort = django_filters.ChoiceFilter(
#         empty_label=None,
#         label='Sort',
#         choices=constants.PROSPECT_SORT_CHOICES,
#         method='filter_none',
#         widget=forms.RadioSelect(
#             attrs={'class': 'form-check-input filter-select'}))

#     def __init__(self, *args, **kwargs):
#         self.budget_id = kwargs.pop('budget_id', None)
#         super(ProspectFilter, self).__init__(*args, **kwargs)
#         self.form.fields[
#             'payment_accounts'].choices = get_payment_account_list(self.budget_id)
#         self.form.fields[
#             'expenditure_heads'].choices = get_expenditure_head_list(self.budget_id)

    
#     def filter_none(self, queryset, name, value):
#         return queryset


#     def filter_by_custom_date_range(self, queryset, name, value):
#         if self.data.get('date_range') == 'custom':
#             start_date = self.data.get('start_date')
#             end_date = self.data.get('end_date')
#             if start_date and end_date:
#                 return queryset.filter(
#                     payment_date__range=[start_date, end_date])
#         return queryset

