from rest_framework import serializers
from elmedi.constants import *
from ..models import ContractCustomer, Contract, Program
from customer.models import Customer
from directory.models import ICD, Hospital, Insurance, Insurer
from package_icd_management.models import PackageICD
from elmedi.constants import TYPE_APPEAL_CHOICES, PLACE_CHOICES
from hospital_icd_management.models import HospitalPackageICD


class PerformedServiceSerializer(serializers.Serializer):
    card_number = serializers.SlugRelatedField(
        queryset=ContractCustomer.objects.all(), slug_field='number')
    hospital = serializers.SlugRelatedField(
        queryset=Hospital.objects.all(), slug_field='code')
    icd = serializers.SlugRelatedField(
        queryset=ICD.objects.all(), slug_field='code'
    )
    type_appeal = serializers.ChoiceField(choices=TYPE_APPEAL_CHOICES, allow_null=True)
    place = serializers.ChoiceField(choices=PLACE_CHOICES, allow_null=True)

    def validate(self, data):
        # card_number = data.get('card_number')
        # hospital = data.get('hospital')
        icd = data.get('icd', None)
        type_appeal = data.get('type_appeal', None)
        place = data.get('place', None)
        if type_appeal and place:
            field_name = package_icd_field_names[type_appeal-1][place-1]
            package_icd_availability = PackageICD.check_availability(icd, field_name)
            hospital_package_icd_availability = HospitalPackageICD.check_availability(icd, field_name)
            if not package_icd_availability:
                raise serializers.ValidationError(
                    "Указанный мкб-10 исключается")
            if not hospital_package_icd_availability:
                raise serializers.ValidationError(
                    "Выбранная больница не выполняет указанный мкб-10")
        return data


class ContractSerializer(serializers.ModelSerializer):
    insurance = serializers.SlugRelatedField(
        queryset=Insurance.objects.all(), slug_field='title')
    insurer = serializers.SlugRelatedField(
        queryset=Insurer.objects.all(), slug_field='title')

    class Meta:
        model = Contract
        fields = ['insurance', 'insurer']


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ['title']


# Сериализатор направления
class ContractCustomerSerializer(serializers.ModelSerializer):
    program = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
     )
    contract = ContractSerializer(
        read_only=True
     )

    class Meta:
        model = ContractCustomer
        fields = ['contract', 'number', 'begin_date', 'end_date', 'type_holder',
            'program', 'customer', 'invoice_sum', 'limit_sum']
