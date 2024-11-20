from datetime import datetime, timedelta
from django.db.models import Sum
from django import template
from ..models import PackageService

register = template.Library()


@register.simple_tag
def is_service_in_package(package, service):
    package_service_exists = PackageService.objects.filter(package=package, service=service).exists()
    result = 1 if package_service_exists else 0
    return result


@register.simple_tag
def get_restriction(package):
    package_services = PackageService.objects.filter(
        package=package).aggregate(Sum('vhi_price'))
    return package_services.get('vhi_price__sum', 0)

@register.simple_tag
def get_program_restriction(program):
    package_services = PackageService.objects.filter(
        package__program=program).aggregate(Sum('vhi_price'))
    return package_services.get('vhi_price__sum', 0)


@register.simple_tag
def get_package_service(package, service):
    package_service = PackageService.objects.filter(package=package, service=service).first()
    if package_service:
        return package_service
    return ''


@register.simple_tag
def get_price(val1, val2):
    if val1 == val2:
        return 'selected'
    return ''


@register.simple_tag
def get_program_package_service(program, service):
    return PackageService.objects.filter(
            package__program=program, service=service).first()
