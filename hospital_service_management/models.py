from django.db import models
from .abstract_models import HospitalPackageMixin, HospitalPackageServiceMixin


# Пакеты
class HospitalPackage(HospitalPackageMixin):
    pass


# Услуги пакета
class HospitalPackageService(HospitalPackageServiceMixin):
    hospital_package = models.ForeignKey(HospitalPackage, on_delete=models.CASCADE)

