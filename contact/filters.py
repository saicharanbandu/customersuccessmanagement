import django_filters
from django.db.models import Q
from .models import Contact
from tabernacle_customer_success import constants
class ContactFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")
    sort = django_filters.ChoiceFilter(choices=[(key, value) for key, value in constants.contact_sort_options.items()], required=False, label="Sort")

    class Meta:
        model = Contact
        fields = ['search']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(organization__icontains=value)
        )
