from rest_framework import serializers
from elmedi.constants import *
from ..models import Referral
from customer.models import Customer
from directory.models import Service, ICD, Hospital
from contract_management.models import ContractCustomer
from package_icd_management.models import PackageICD
from hospital_icd_management.models import HospitalPackageICD


# Сериализатор направления
class ReferralSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field='iin')
    service = serializers.SlugRelatedField(
        queryset=Service.objects.all(), slug_field='code')
    contract_customer = serializers.SlugRelatedField(
        queryset=ContractCustomer.objects.all(), slug_field='number')
    icd = serializers.SlugRelatedField(
        queryset=ICD.objects.all(), slug_field='code')
    sending_hospital = serializers.SlugRelatedField(
        queryset=Hospital.objects.all(), slug_field='code')
    directed_hospital = serializers.SlugRelatedField(
        queryset=Hospital.objects.all(), slug_field='code')

    class Meta:
        model = Referral
        fields = [
            'id', 'customer', 'sending_hospital', 'directed_hospital',
            'service', 'doctor_full_name', 'date',
            'cancel_date', 'contract_customer', 'icd', 'status',
            'type_appeal', 'place'
        ]

    # def validate(self, data):
    #     customer = data['customer']
    #     contract_customer = data['contract_customer']
    #     service = data['service']
    #     icd = data['icd']
    #     directed_hospital = data['directed_hospital']
    #     type_appeal = data['type_appeal']
    #     place = data['place']
    #     check_availability = contract_customer.check_availability()
    #     if not check_availability.get('status'):
    #         raise serializers.ValidationError(
    #             check_availability.get('message'))
    #     field_name = package_icd_field_names[type_appeal - 1][place - 1]
    #     package_icd_availability = PackageICD.check_availability(icd, field_name)
    #     hospital_package_icd_availability = HospitalPackageICD.check_availability(icd, field_name)
    #     if package_icd_availability:
    #         raise serializers.ValidationError(
    #             "Указанный мкб-10 исключается")
    #     if hospital_package_icd_availability:
    #         raise serializers.ValidationError(
    #             "Выбранная больница не выполняет указанный мкб-10")
    #     return data

