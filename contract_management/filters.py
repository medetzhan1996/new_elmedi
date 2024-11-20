import django_filters
from .models import ContractCustomer

class ContractCustomerFilter(django_filters.FilterSet):
    customer__iin = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Invoice
        fields = ['contract__insurance', 'program', 'customer__iin']