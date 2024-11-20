import django_filters
from invoice_management.models import Invoice


class InvoiceFilter(django_filters.FilterSet):
    contract_customer__customer__iin = django_filters.CharFilter(lookup_expr='icontains')
    contract_customer__number = django_filters.CharFilter(lookup_expr='icontains')
    service__title = django_filters.CharFilter(lookup_expr='icontains')
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Invoice
        fields = ['service__title', 'date__gte', 'date__lte', 'contract_customer__customer__iin',
                  'contract_customer__number']
