from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerSerializer
from ..models import Customer


# Посмотреть список или создать направление
class CustomerSearch(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        search = self.kwargs['search']
        customer = Customer.objects.filter(customer__iin=search).first()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
