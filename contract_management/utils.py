from contract_management.models import HospitalPackageService
from elmedi.constants import package_service_field_names


def get_performed_services(hospital, program, type_appeal=None, place=None):
    if type_appeal and place:
        package_services = HospitalPackageService.objects.filter(
            service__children__isnull=True,
            hospital_package__contract_hospital__program=program)
        field_name = package_service_field_names[type_appeal - 1][place - 1]
        package_services = package_services.filter(**{field_name: False})
    return package_services.values_list('service')
