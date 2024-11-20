from contract_management.models import ContractCustomer, Package
from promedicine.models import ExaminationAppointment, ProfessionalExamination, ExaminationResult
from promedicine.api.serializers import ExaminationAppointmentSerializer, ExaminationResultSerializer, \
    ExaminationResultListSerializer, PackageListSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfessionalExaminationApiView(APIView):

    def get(self, request, *args, **kwargs):
        iin = kwargs.get('iin')
        professional_examinations = ProfessionalExamination.objects.filter(contract_customer__customer__iin=iin)
        print(professional_examinations)
        response_data = []

        for professional_examination in professional_examinations:
            professional_examination_services = professional_examination.examinationappointment_set.all()
            service_data = []

            for appointment in professional_examination_services:
                service_data.append({
                    "id": appointment.id,
                    "service_id": appointment.service.id,
                    "service_title": appointment.service.title,
                    "doctor_code": appointment.doctor_code,
                    "date_time": appointment.date_time,
                    "status": appointment.status
                })

            data = {
                'first_name': professional_examination.contract_customer.customer.first_name,
                'last_name': professional_examination.contract_customer.customer.last_name,
                'iin': professional_examination.contract_customer.customer.iin,
                'services': service_data,
                'contract': professional_examination.contract_customer.contract.number,
                'program': professional_examination.contract_customer.program.title,
            }

            response_data.append(data)

        return Response({'Data': response_data})


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ExaminationAppointmentApiView(APIView):

    def get(self, request, *args, **kwargs):
        iin = kwargs.get('customer_iin')
        if not iin:
            return Response({'Error': 'Customer IIN not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        professional_examinations = ProfessionalExamination.objects.filter(contract_customer__customer__iin=iin)
        if not professional_examinations.exists():
            return Response({'Error': 'No examinations found for the given IIN.'}, status=status.HTTP_404_NOT_FOUND)

        examination_appointments = ExaminationAppointment.objects.filter(
            professional_examination__in=professional_examinations)
        serializer = ExaminationAppointmentSerializer(examination_appointments, many=True)
        return Response({'Data': serializer.data}, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ExaminationResultApiView(APIView):

    def get(self, request, *args, **kwargs):
        iin = kwargs.get('customer_iin')
        if not iin:
            return Response({'Error': 'Customer IIN not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        professional_examinations = ProfessionalExamination.objects.filter(contract_customer__customer__iin=iin)
        if not professional_examinations.exists():
            return Response({'Error': 'No examinations found for the given IIN.'}, status=status.HTTP_404_NOT_FOUND)

        examination_results = ExaminationResult.objects.filter(
            examination_appointment__professional_examination__in=professional_examinations)
        serializer = ExaminationResultListSerializer(examination_results, many=True)
        return Response({'Data': serializer.data}, status=status.HTTP_200_OK)


class ExaminationResultCreateView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ExaminationResultSerializer

# class ExaminationResultCreateView(APIView):
#
#     def post(self, request):
#         serializer = ExaminationResultSerializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class PackageListApiView(APIView):

    def get(self, request, *args, **kwargs):
        iin = kwargs.get('customer_iin')
        if not iin:
            return Response({'Error': 'Customer IIN not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        programs = ContractCustomer.objects.filter(customer__iin=iin).values_list('program', flat=True)
        if not programs.exists():
            return Response({'Error': 'No programs found for the given IIN.'}, status=status.HTTP_404_NOT_FOUND)

        packeges = Package.objects.filter(
            program__in=programs)
        serializer = PackageListSerializer(packeges, many=True)
        return Response({'Data': serializer.data}, status=status.HTTP_200_OK)