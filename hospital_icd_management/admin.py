from django.contrib import admin
from .models import HospitalPackage, HospitalPackageICD

admin.site.register(HospitalPackage)
admin.site.register(HospitalPackageICD)
