from django import template
from ..models import HospitalPackageService

register = template.Library()


@register.simple_tag
def get_hospital_package_service(hospital, service, hospital_package=None):
    hospital_package_service = HospitalPackageService.objects.filter(
        hospital_package__hospital=hospital, service=service)
    if hospital_package:
        hospital_package_service = hospital_package_service.filter(
            hospital_package=hospital_package)
    return hospital_package_service.first()
