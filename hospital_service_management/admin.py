from django.contrib import admin
from .models import HospitalPackage, HospitalPackageService

admin.site.register(HospitalPackage)
admin.site.register(HospitalPackageService)
