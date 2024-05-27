import django_filters
from django.db.models import Q
from .models import Profile
from tabernacle_customer_success import constants

class ProfileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")
    status = django_filters.MultipleChoiceFilter(method='filter_status',choices=constants.PROSPECT_STATUS_CHOICES)
    sort = django_filters.ChoiceFilter(choices=[(key, value) for key, value in constants.PROSPECT_SORT_CHOICES.items()], required=False, label="Sort")

    class Meta:
        model = Profile
        fields = ['search', 'status']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))
    
    def filter_status(self, queryset, name, value):
        print(value)
        if value[0]=="all":
            return queryset
        else:
            queryset = queryset.filter(status__in=value)
            return queryset
    def filter_by_order(self, queryset, name, value):
        sort_field = constants.PROSPECT_SORT_CHOICES.get(value, '')
        if sort_field:
            queryset = queryset.order_by(sort_field)
        return queryset