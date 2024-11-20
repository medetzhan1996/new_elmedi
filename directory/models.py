from django.db import models
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields
from mptt.models import MPTTModel, TreeForeignKey


class TranslatableTreeQuerySet(TreeQuerySet, TranslatableQuerySet):
    pass

# Базовый mixin
class BaseMixin(models.Model):
    title = models.CharField(max_length=320)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


# Услуги
class Service(TranslatableModel, MPTTModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=320)
    )
    code = models.CharField(max_length=180, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    objects = TranslatableTreeQuerySet.as_manager()


# Услуги
class Form(TranslatableModel, MPTTModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=320)
    )
    code = models.CharField(max_length=180, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    file = models.FileField(upload_to='documents/', blank=True, null=True)


# Страховка государства 
class StateInsurance(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    is_impossible = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    at_home_coefficient = models.FloatField(null=True, blank=True)
    primary_health_care_coefficient = models.FloatField(null=True, blank=True)
    clinical_diagnostic_coefficient = models.FloatField(null=True, blank=True)
    hospital_coefficient = models.FloatField(null=True, blank=True)


# Страховая компания
class Insurance(BaseMixin):
    logo = models.ImageField(upload_to='documents/', blank=True, null=True)
    bin = models.CharField(max_length=180, null=True, blank=True)
    address = models.CharField(max_length=180, null=True, blank=True)
    iik = models.CharField(max_length=180, null=True, blank=True)
    bik = models.CharField(max_length=180, null=True, blank=True)
    phone_number = models.CharField(max_length=180, null=True, blank=True)
    residency = models.CharField(max_length=180, null=True, blank=True)
    sector_economy = models.CharField(max_length=180, null=True, blank=True)
    code = models.CharField(max_length=180)
    is_checked = models.BooleanField(default=True)


# Страховщик
class Insurer(BaseMixin):
    bin = models.CharField(max_length=180, null=True, blank=True)
    address = models.CharField(max_length=180, null=True, blank=True)
    iik = models.CharField(max_length=180, null=True, blank=True)
    bik = models.CharField(max_length=180, null=True, blank=True)
    phone_number = models.CharField(max_length=180, null=True, blank=True)
    residency = models.CharField(max_length=180, null=True, blank=True)
    sector_economy = models.CharField(max_length=180, null=True, blank=True)


# Больницы
class Hospital(BaseMixin):
    logo = models.ImageField(upload_to='documents/', blank=True, null=True)
    address = models.CharField(max_length=180, null=True, blank=True)
    code = models.CharField(max_length=180)
    is_checked = models.BooleanField(default=True)

    def is_service_performed(self, service):
        return self.hospitalpackage_set.filter(
            hospitalpackageservice__service=service).exists()


# Список отделении
class FuncStructure(BaseMixin):
    pass


# МКБ-10
class ICD(TranslatableModel, MPTTModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=320)
    )
    code = models.CharField(max_length=180, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    is_impossible = models.BooleanField(default=False)
    objects = TranslatableTreeQuerySet.as_manager()
