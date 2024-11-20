from datetime import datetime, timedelta
from django.db.models import Sum
from django import template
from ..models import PackageICD, Package

register = template.Library()


@register.simple_tag
def is_icd_in_package(package, icd):
    package_icd_exists = PackageICD.objects.filter(package=package, icd=icd).exists()
    result = 1 if package_icd_exists else 0
    return result


@register.simple_tag
def get_package_icd(package, icd):
    package_icd = PackageICD.objects.filter(package=package, icd=icd).first()
    if package_icd:
        return package_icd
    return ''


@register.simple_tag
def get_icd(icd):
    package_icd = PackageICD.objects.filter(icd=icd, is_perfomed=True).first()
    if package_icd:
        return package_icd
    return ''


@register.simple_tag
def get_package(package):
    if package:
        return package
    package = Package.objects.filter(is_favorite=False).first()
    if package:
        return package.id