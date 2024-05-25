import django_filters
from django.db.models import Q
from .models import Profile
from tabernacle_customer_success import constants

class ProfileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")
    status = django_filters.ChoiceFilter(choices=constants.PROSPECT_STATUS_CHOICES)

    class Meta:
        model = Profile
        fields = ['search', 'status']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))
