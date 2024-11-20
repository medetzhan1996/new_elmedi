from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from .serializers import CustomerSerializer
from ..models import Customer


# Mixin клиента
class CustomerMixin:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'iin'


# Создать нового клиента
class CustomerCreateView(CustomerMixin, CreateAPIView):
    pass