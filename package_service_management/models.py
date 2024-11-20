from django.db import models
from directory.models import Insurer
from .abstract_models import PackageMixin, PackageServiceMixin


# Пакеты
class Package(PackageMixin):
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, null=True, blank=True)


# Услуги пакета
class PackageService(PackageServiceMixin):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
