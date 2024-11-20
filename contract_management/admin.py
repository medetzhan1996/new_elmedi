from django.contrib import admin
from .models import ContractCustomer, ContractHospital, \
    Program, Package, PackageService, Contract, HospitalPackage, HospitalPackageService

admin.site.register(ContractCustomer)
admin.site.register(ContractHospital)
admin.site.register(PackageService)
admin.site.register(Contract)
admin.site.register(Program)
admin.site.register(Package)
admin.site.register(HospitalPackage)
admin.site.register(HospitalPackageService)









