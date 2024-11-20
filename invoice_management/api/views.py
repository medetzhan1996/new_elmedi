from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import InvoiceSerializer, InvoiceEPSDMSSerializer
from ..models import Invoice, InvoiceEPSDMS


class InvoiceMixin:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


# Посмотреть список направлении
class InvoiceCreateView(InvoiceMixin, generics.CreateAPIView):
    name = 'invoice-create'


# Посмотреть детальную информацию направления
class InvoiceDetail(InvoiceMixin, generics.RetrieveUpdateDestroyAPIView):
    name = 'invoice-detail'


class InvoiceEPSDMSMixin:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = InvoiceEPSDMSSerializer
    queryset = InvoiceEPSDMS.objects.all()


# Посмотреть список направлении
class InvoiceEPSDMSCreateView(InvoiceEPSDMSMixin, generics.CreateAPIView):
    name = 'invoice-eps_dms-create'