import random
import string

from datetime import date
from django.db import models
from django.db.models import Sum
from directory.models import Insurer, Insurance, Hospital
from customer.models import Customer
from program_management.abstract_models import ProgramMixin
from package_service_management.abstract_models import PackageMixin, PackageServiceMixin
from hospital_service_management.abstract_models import HospitalPackageMixin, HospitalPackageServiceMixin
from directory.models import Service
from django.utils.translation import gettext_lazy as _


# Программа
class Contract(models.Model):
    VOLUNTARY_INSURANCE = 1
    PROFESSIONAL_INSURANCE = 2

    INSURANCE_TYPE_CHOICES = [
        (VOLUNTARY_INSURANCE, _('Добровольное медицинское страхование')),
        (PROFESSIONAL_INSURANCE, _('профессиональное медицинское страхование'))
    ]
    insurance_type = models.IntegerField(choices=INSURANCE_TYPE_CHOICES, default=VOLUNTARY_INSURANCE)
    number = models.CharField(max_length=180, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    # Получить сумму премии
    def get_premium_sum(self):
        query = self.program_set.aggregate(
            Sum('program__insurance_premium')).get('program__insurance_premium__sum') or 0
        return query

    # Получить сумму страховки
    def get_insurance_sum(self):
        query = self.contractprogram_set.aggregate(
            Sum('program__insurance_limit')).get('program__insurance_limit__sum') or 0
        return query


# Программа
class Program(ProgramMixin):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def get_limit(self):
        query = self.package_set.aggregate(Sum('limit')).get('limit__sum') or 0
        return query

    @property
    def service_limit(self):
        limit_sum = 0
        for package in self.package_set.all():
            limit_sum = limit_sum + package.service_limit
        return limit_sum


# Пакеты
class Package(PackageMixin):
    LIMIT_TYPE_CHOICES_PRIMARY = 1
    LIMIT_TYPE_CHOICES_PARENT = 2
    LIMIT_TYPE_CHOICES_SPOUSE = 3

    LIMIT_TYPE_CHOICES = [
        (LIMIT_TYPE_CHOICES_PRIMARY, _('Полное покрытие')),
        (LIMIT_TYPE_CHOICES_PARENT, _('Лимит на стоимость услуг')),
        (LIMIT_TYPE_CHOICES_SPOUSE, _('Лимит на количество услуг')),    
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    limit_type = models.IntegerField(choices=LIMIT_TYPE_CHOICES, default=1)

    @property
    def service_limit(self):
        return self.packageservice_set.aggregate(Sum('vhi_price')).get('vhi_price__sum') or 0


# Услуги пакета
class PackageService(PackageServiceMixin):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


# Застрахованный клиент
class ContractCustomer(models.Model):
    TYPE_HOLDER_PRIMARY = 1
    TYPE_HOLDER_PARENT = 2
    TYPE_HOLDER_SPOUSE = 3
    TYPE_HOLDER_CHILDREN = 4

    TYPE_HOLDER_CHOICES = [
        (TYPE_HOLDER_PRIMARY, _('Основной держатель')),
        (TYPE_HOLDER_PARENT, _('Родитель')),
        (TYPE_HOLDER_SPOUSE, _('Супруга')),
        (TYPE_HOLDER_CHILDREN, _('Дети')),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    number = models.CharField(max_length=80, unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    type_holder = models.IntegerField(choices=TYPE_HOLDER_CHOICES, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    base_card = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Если это новый экземпляр и код не задан
        if not self.pk and not self.number:
            self.number = self.generate_unique_code()
        super(ContractCustomer, self).save(*args, **kwargs)

    def generate_unique_code(self):
        number = self.generate_code()
        while ContractCustomer.objects.filter(number=number).exists():
            number = self.generate_code()
        return number

    @staticmethod
    def generate_code(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def check_availability(self):
        data = {'status': True}
        today = date.today()
        if self.end_date < today:
            data['status'] = False
            data['message'] = 'Указанная карта не действительная'
        return data

    # Получить сумму счет реестра
    def get_invoice_sum(self):
        result = 0
        invoices = self.invoice_set.all()
        for invoice in invoices:
            result = result + invoice.service_consumption
        return result

    @property
    def invoice_sum(self):
        result = 0
        invoices = self.invoice_set.all()
        for invoice in invoices:
            result = result + invoice.service_consumption
        return result

    @property
    def limit_sum(self):
        return self.program.service_limit

    # Получить сумму счет реестра
    def get_invoice_sum(self):
        consumption_sum = self.invoice_set.aggregate(
            Sum('consumption')).get('consumption__sum') or 0
        return consumption_sum

    def get_available_hospitals(self):
        return self.contract.contracthospital_set.values('hospital__title', 'hospital__code')

    def __str__(self):
        return self.number


# Застрахованный клиент
class ContractHospital(models.Model):
    STATUS_CHOICES = [
        (1, 'Отправить'),
        (2, 'Отправлен'),
        (3, 'Заявка принята'),
        (4, 'Заявка переотправлена')
    ]
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)


# Пакеты
class HospitalPackage(HospitalPackageMixin):
    STATUS_CHOICES = [
        (1, 'Ожидание'),
        (2, 'Заявка страховой компании'),
        (3, 'Подтверждение провайдера'),
        (4, 'Контракт'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    contract_hospital = models.ForeignKey(ContractHospital, on_delete=models.CASCADE)


# Услуги пакета
class HospitalPackageService(HospitalPackageServiceMixin):
    hospital_package = models.ForeignKey(HospitalPackage, on_delete=models.CASCADE)
    hospital_at_home_coefficient = models.FloatField(null=True, blank=True)
    hospital_primary_health_care_coefficient = models.FloatField(null=True, blank=True)
    hospital_clinical_diagnostic_coefficient = models.FloatField(null=True, blank=True)
    hospital_hospital_coefficient = models.FloatField(null=True, blank=True)
    hospital_price = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    insurance_at_home_coefficient = models.FloatField(null=True, blank=True)
    insurance_primary_health_care_coefficient = models.FloatField(null=True, blank=True)
    insurance_clinical_diagnostic_coefficient = models.FloatField(null=True, blank=True)
    insurance_hospital_coefficient = models.FloatField(null=True, blank=True)
    insurance_base_price = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)



