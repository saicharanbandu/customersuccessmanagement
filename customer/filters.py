import django_filters
from django.db.models import Q
from . import models as customerModels
from tabernacle_customer_success import constants


class CustomerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")
    plan_status = django_filters.MultipleChoiceFilter(method='filter_status', choices=constants.CUSTOMER_PLAN_STATUS_CHOICES)
    payment_status = django_filters.MultipleChoiceFilter(method='filter_payment_status', choices=constants.CUSTOMER_Payment_STATUS_CHOICES)
    sort = django_filters.ChoiceFilter(method='filter_sort', choices=[(key, value) for key, value in constants.customer_sort_options.items()], required=False, label="Sort")

    class Meta:
        model = customerModels.SubscribedPlan
        fields = ['search', 'plan_status', 'sort']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(Q(official_name__icontains=value))

    def filter_status(self, queryset, name, value):
        print(value)
        if value[0] == "all":
            return queryset
        else:
            
            queryset = queryset.filter(customer_plan__subscription_plan__name__in=value)
            print(queryset)
            return queryset
    def filter_payment_status(self, queryset, name, value):
        print(value)
        if value[0] == "all":
            return queryset
        else:
            
            queryset = queryset.filter(customer_plan__subscription_plan__name__in=value)
            print(queryset)
            return queryset
    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by(constants.customer_sort_options.get(value, '-created_at'))
        return queryset