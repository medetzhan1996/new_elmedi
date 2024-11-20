from django.db import models
from directory.models import Service, ICD
from elmedi.constants import TYPE_APPEAL_CHOICES, PLACE_CHOICES
from contract_management.models import ContractCustomer, HospitalPackageService
from referral_management.models import Referral
from directory.models import Hospital


# Счет реестр пациента
class Invoice(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    icd = models.ForeignKey(ICD, on_delete=models.CASCADE)
    contract_customer = models.ForeignKey(ContractCustomer, on_delete=models.CASCADE)
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    consumption = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    screen = models.TextField(blank=True, null=True)
    performing_doctor = models.CharField(max_length=180, blank=True, null=True)
    doctor_signature = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    type_appeal = models.IntegerField(choices=TYPE_APPEAL_CHOICES)
    place = models.IntegerField(choices=PLACE_CHOICES)

    @property
    def service_consumption(self):
        program = self.contract_customer.program
        package_service = HospitalPackageService.objects.filter(
            hospital_package__contract_hospital__program=program, service=self.service).last()
        return package_service.vhi_price  or 0



# Счет реестр пациента
class InvoiceEPSDMS(models.Model):
    service = models.CharField(max_length=320)
    icd = models.CharField(max_length=320)
    full_name = models.CharField(max_length=320)
    iin = models.CharField(max_length=320)
    contract_customer = models.CharField(max_length=320)
    referral = models.CharField(max_length=320, blank=True, null=True)
    hospital = models.CharField(max_length=320, blank=True, null=True)
    consumption = models.CharField(max_length=320, blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    performing_doctor = models.CharField(max_length=180, blank=True, null=True)
    doctor_signature = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    type_appeal = models.IntegerField(choices=TYPE_APPEAL_CHOICES)
    place = models.IntegerField(choices=PLACE_CHOICES)

