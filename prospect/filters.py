import django_filters
from django.db.models import Q
from .models import Profile
from tabernacle_customer_success import constants


class ProfileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")
    status = django_filters.MultipleChoiceFilter(method='filter_status', choices=constants.PROSPECT_STATUS_CHOICES)
    sort = django_filters.ChoiceFilter(method='filter_sort', choices=[(key, value) for key, value in constants.PROSPECT_SORT_CHOICES.items()], required=False, label="Sort")

    class Meta:
        model = Profile
        fields = ['search', 'status', 'sort']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    def filter_status(self, queryset, name, value):
        if value[0] == "all":
            return queryset
        else:
            queryset = queryset.filter(status__in=value)
            return queryset

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by(constants.PROSPECT_SORT_CHOICES.get(value, '-created_at'))
        return queryset