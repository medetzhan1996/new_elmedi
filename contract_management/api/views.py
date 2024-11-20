import requests
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from directory.models import Service
from directory.api.serializers import ServiceSerializer
from contract_management.models import Contract, Program
from contract_management.utils import get_performed_services
from promedicine.models import ProfessionalExamination, SpecialityService, ExaminationAppointment
from ..models import ContractCustomer
from .serializers import PerformedServiceSerializer, ContractCustomerSerializer, ProgramSerializer


class PerformedServicesView(APIView):

    def post(self, request):
        results = PerformedServiceSerializer(data=request.data)
        if results.is_valid(raise_exception=True):
            card_number = request.data.get('card_number')
            hospital = request.data.get('hospital')
            type_appeal = int(request.data.get('type_appeal', None))
            place = int(request.data.get('place', None))
            contract_customer = ContractCustomer.objects.get(number=card_number)
            program = contract_customer.program
            performed_services = get_performed_services(
                hospital, program, type_appeal, place)
            services = Service.objects.filter(id__in=performed_services)
            results = ServiceSerializer(services, many=True)
        return Response(results.data)


class AvailableHospitalsView(APIView):

    def get(self, request, *args, **kwargs):
        card_number = kwargs.get('card_number')
        contract_customer = ContractCustomer.objects.get(number=card_number)
        available_hospitals = contract_customer.get_available_hospitals()
        return Response(available_hospitals)


class ContractCustomerCreateView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ContractCustomerSerializer
    queryset = ContractCustomer.objects.all()


class ContractCustomerDetailView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ContractCustomerSerializer
    queryset = ContractCustomer.objects.all()
    lookup_field = 'number'


# Посмотреть список или создать направление
class CustomerContractListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        search = self.kwargs['search']
        contract_customer = ContractCustomer.objects.filter(customer__iin=search).all()
        serializer = ContractCustomerSerializer(contract_customer, many=True)
        return Response(serializer.data)


class ProgramListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)






