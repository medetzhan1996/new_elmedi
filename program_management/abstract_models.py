from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class ProgramMixin(models.Model):
    title = models.CharField(max_length=180)
    is_favorite = models.BooleanField(default=False)
    limit_percent = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)
    premium_percent = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)

    class Meta:
        ordering = ['id']
        abstract = True

    def __str__(self):
        return self.title

    # Проверить выполняется ли указанная услуга
    def is_service_performed(self, service):
        return self.programpackage_set.filter(
            package__packageservice__service=service).exists()


class ProgramPackageMixin(models.Model):
    LIMIT_TYPE_CHOICES = [
        (1, 'Полное покрытие'),
        (2, 'Лимит на стоимость услуг'),
        (3, 'Лимит на количество услуг')
    ]
    limit = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    limit_type = models.IntegerField(choices=LIMIT_TYPE_CHOICES, default=1)

    def __str__(self):
        return self.package.title

    class Meta:
        ordering = ['id']
        abstract = True
