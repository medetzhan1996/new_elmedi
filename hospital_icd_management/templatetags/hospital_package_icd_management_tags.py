from datetime import datetime, timedelta
from django.db.models import Sum
from django import template
from ..models import HospitalPackageICD

register = template.Library()


@register.simple_tag
def get_hospital_package_icd(hospital_package, icd):
    hospital_package_service = HospitalPackageICD.objects.filter(
        hospital_package=hospital_package, icd=icd).first()
    if hospital_package_service:
        return hospital_package_service
    return ''

