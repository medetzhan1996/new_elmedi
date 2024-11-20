from django.db import models
from directory.models import Service


class PackageMixin(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related',
        null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


# Базовый mixin пакета услуг
class PackageServiceMixin(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    state_at_home = models.FloatField(null=True, blank=True)
    state_primary_health_care = models.FloatField(null=True, blank=True)
    state_clinical_diagnostic = models.FloatField(null=True, blank=True)
    state_hospital = models.FloatField(null=True, blank=True)
    vhi_at_home_coefficient = models.FloatField(null=True, blank=True)
    vhi_primary_health_care_coefficient = models.FloatField(null=True, blank=True)
    vhi_clinical_diagnostic_coefficient = models.FloatField(null=True, blank=True)
    vhi_hospital_coefficient = models.FloatField(null=True, blank=True)
    vhi_price = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    pay_at_home_coefficient = models.FloatField(null=True, blank=True)
    pay_primary_health_care_coefficient = models.FloatField(null=True, blank=True)
    pay_clinical_diagnostic_coefficient = models.FloatField(null=True, blank=True)
    pay_hospital_coefficient = models.FloatField(null=True, blank=True)
    pay_base_price = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    limit = models.FloatField(null=True, blank=True)
    is_checked = models.BooleanField(default=False)

    class Meta:
        abstract = True