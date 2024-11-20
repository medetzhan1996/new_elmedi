from rest_framework import serializers
from elmedi.constants import *
from ..models import Invoice, InvoiceEPSDMS
from directory.models import Service, ICD, Hospital
from package_icd_management.models import PackageICD
from hospital_icd_management.models import HospitalPackageICD
from contract_management.models import ContractCustomer


# Сериализатор направления
class InvoiceSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(
        queryset=Service.objects.all(), slug_field='code')
    contract_customer = serializers.SlugRelatedField(
        queryset=ContractCustomer.objects.all(), slug_field='number')
    icd = serializers.SlugRelatedField(
        queryset=ICD.objects.all(), slug_field='code')
    hospital = serializers.SlugRelatedField(
        queryset=Hospital.objects.all(), slug_field='code')

    class Meta:
        model = Invoice
        fields = [
            'id', 'service', 'icd', 'contract_customer',
            'referral', 'hospital', 'consumption',
            'performing_doctor', 'place', 'type_appeal',
            'doctor_signature', 'screen'
        ]

    def validate(self, data):
        contract_customer = data['contract_customer']
        service = data['service']
        icd = data['icd']
        type_appeal = data['type_appeal']
        place = data['place']
        check_availability = contract_customer.check_availability()
        if not check_availability.get('status'):
            raise serializers.ValidationError(
                check_availability.get('message'))
        field_name = package_icd_field_names[type_appeal - 1][place - 1]
        package_icd_availability = PackageICD.check_availability(icd, field_name)
        hospital_package_icd_availability = HospitalPackageICD.check_availability(icd, field_name)
        if not package_icd_availability:
            raise serializers.ValidationError(
                "Указанный мкб-10 исключается")
        if not hospital_package_icd_availability:
            raise serializers.ValidationError(
                "Выбранная больница не выполняет указанный мкб-10")
        return data


# # Сериализатор направления
# class HospitalServicesSerializer(serializers.Serializer):
#     services = serializers.SlugRelatedField(
#         queryset=Service.objects.all(), slug_field='code', many=True)

class InvoiceEPSDMSSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InvoiceEPSDMS
        fields = [
            'id', 'service', 'icd', 'contract_customer',
            'referral', 'hospital', 'consumption',
            'performing_doctor', 'place', 'type_appeal',
            'doctor_signature', 'screen', 'full_name', 'iin'
        ]