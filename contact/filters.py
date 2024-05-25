import django_filters
from django.db.models import Q
from .models import Contact

class ContactFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label="Search")

    class Meta:
        model = Contact
        fields = ['search']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(organization__icontains=value)
        )
