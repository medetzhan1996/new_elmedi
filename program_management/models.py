from django.db import models
from program_management.abstract_models import ProgramMixin
from directory.models import Insurer
from package_service_management.abstract_models import PackageMixin, PackageServiceMixin
from django.utils.translation import gettext_lazy as _


# Программа
class Program(ProgramMixin):
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, null=True, blank=True)
    PROGRAM_TYPE_CHOICES = [
        (1, 'ДМС'),
        (2, 'ОМО'),
        (3, 'ОПМО')
    ]
    program_type = models.IntegerField(choices=PROGRAM_TYPE_CHOICES, default=1)


# Пакеты
class Package(PackageMixin):
    LIMIT_TYPE_PRIMARY = 1
    LIMIT_TYPE_PARENT = 2
    LIMIT_TYPE_SPOUSE = 3

    LIMIT_TYPE_CHOICES = [
        (LIMIT_TYPE_PRIMARY, _('Полное покрытие')),
        (LIMIT_TYPE_PARENT, _('Лимит на стоимость услуг')),
        (LIMIT_TYPE_SPOUSE, _('Лимит на количество услуг')),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    limit_type = models.IntegerField(choices=LIMIT_TYPE_CHOICES, default=1)


# Услуги пакета
class PackageService(PackageServiceMixin):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

