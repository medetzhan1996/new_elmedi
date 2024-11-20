from datetime import datetime, timedelta
from django.db.models import Sum
from django import template
from directory.models import Hospital, Service
from ..models import ContractCustomer, PackageService, HospitalPackageService, Contract, ContractHospital

register = template.Library()


@register.simple_tag
def is_service_performed(hospital, service):
    return hospital.is_service_performed(service)


@register.simple_tag
def get_contract_customer_count(contract, type_holder=False):
    query = ContractCustomer.objects.filter(contract=contract)
    if type_holder and type_holder == 'employee':
        query = query.filter(type_holder=1)
    elif type_holder and type_holder == 'family':
        query = query.exclude(type_holder=1)
    return query.count()


@register.simple_tag
def get_program_restriction(program):
    package_services = PackageService.objects.filter(
        package__program=program).aggregate(Sum('vhi_price'))
    return package_services.get('vhi_price__sum', 0)


@register.simple_tag
def get_price(val1, val2):
    if val1 == val2:
        return 'selected'
    return ''


@register.simple_tag
def get_restriction(package):
    package_services = PackageService.objects.filter(
        package=package).aggregate(Sum('vhi_price'))
    return package_services.get('vhi_price__sum', 0)


@register.simple_tag
def get_program_package_service(program, service):
    return PackageService.objects.filter(
            package__program=program, service=service).first()


@register.simple_tag
def get_val_by_percent(val, perc):
   if perc:
       return float(val)*float((perc/100))


@register.simple_tag
def get_contract_hospital_package_service(hospital_package, service):
    return HospitalPackageService.objects.filter(
        hospital_package=hospital_package,
        service=service).first()


@register.simple_tag
def get_contract_hospital_package_services(hospital_package):
    hospital_services = HospitalPackageService.objects.filter(
            hospital_package=hospital_package).values_list('service', flat=True)
    return Service.objects.filter(id__in=hospital_services)

@register.simple_tag
def get_contract_hospital_service(contract_hospital, service):
    return HospitalPackageService.objects.filter(
        hospital_package__contract_hospital=contract_hospital,
        service=service).first()



@register.simple_tag
def get_contract(pk):
    return Contract.objects.get(pk=pk)


@register.simple_tag
def get_contract_hospital(contract, hospital):
    return ContractHospital.objects.filter(
        contract=contract, hospital=hospital).all()


@register.simple_tag
def get_hospital(pk):
    return Hospital.objects.get(pk=pk)



@register.simple_tag
def is_selected(val1, val2):
    if str(val1) == str(val2):
        return 'selected'
    return ''

@register.filter(name='to_tuple')
def to_tuple(value):
    return tuple(value)