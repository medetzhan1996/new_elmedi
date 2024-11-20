from django.db import models
from directory.models import Hospital, FuncStructure, Insurance
from customer.models import Customer
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES_ONE = 1
    USER_TYPE_CHOICES_TWO = 2
    USER_TYPE_CHOICES_THREE = 3
    USER_TYPE_CHOICES_FOUR = 4
    USER_TYPE_CHOICES_FIVE = 5
    USER_TYPE_CHOICES_SIX = 6
    USER_TYPE_CHOICES_SEVEN = 7
    USER_TYPE_CHOICES_EIGHT = 8
    USER_TYPE_CHOICES_ELEVEN = 11
    USER_TYPE_CHOICES_TWELVE = 12
    USER_TYPE_CHOICES_THIRTEEN= 13
    USER_TYPE_CHOICES_FOURTEEN = 14
    USER_TYPE_CHOICES_FIFTEEN = 15
    USER_TYPE_CHOICES_SIXTEEN = 16
    USER_TYPE_CHOICES_SEVENTEEN = 17
    USER_TYPE_CHOICES_EIGHTTEEN = 18
    USER_TYPE_CHOICES_NINETEEN = 19
    USER_TYPE_CHOICES_TWENTY = 20


    USER_TYPE_CHOICES = [
        (USER_TYPE_CHOICES_ONE, _('КЛИНИЦИСТ')),
        (USER_TYPE_CHOICES_TWO, _('Админ программ')),
        (USER_TYPE_CHOICES_THREE, _('НАСТРОЙКА ПАКЕТОВ')),    
        (USER_TYPE_CHOICES_FOUR, _('Настройка услуг')),    
        (USER_TYPE_CHOICES_FIVE, _('АССИСТАНС')),    
        (USER_TYPE_CHOICES_SIX, _('Страховой контракт')),    
        (USER_TYPE_CHOICES_SEVEN, _('Справочник')),    
        (USER_TYPE_CHOICES_EIGHT, _('Админ контрактов')),    
        (USER_TYPE_CHOICES_ELEVEN, _('Medassitance')),    
        (USER_TYPE_CHOICES_TWELVE, _('Прайскурация/расчеты')),    
        (USER_TYPE_CHOICES_THIRTEEN, _('КЛИНИЦИСТ ОЦЕНКА')),    
        (USER_TYPE_CHOICES_FOURTEEN, _('Настройка мкб-10')),    
        (USER_TYPE_CHOICES_FIFTEEN, _('Настройка мкб-10 ЛПУ')),    
        (USER_TYPE_CHOICES_SIXTEEN, _('Отчет')),    
        (USER_TYPE_CHOICES_SEVENTEEN, _('Админ страховой компании')),    
        (USER_TYPE_CHOICES_EIGHTTEEN, _('Админ больницы')),    
        (USER_TYPE_CHOICES_NINETEEN, _('Админ промедицина')),    
        (USER_TYPE_CHOICES_TWENTY, _('Админ промедицина больницы')),    
    ]
    # USER_TYPE_CHOICES = (
    #     (1, 'КЛИНИЦИСТ'),
    #     (2, 'Админ программ'),
    #     (3, 'НАСТРОЙКА ПАКЕТОВ'),
    #     (4, 'Настройка услуг'),
    #     (7, 'АССИСТАНС'),
    #     (8, 'Страховой контракт'),
    #     (9, 'Справочник'),
    #     (10, 'Админ контрактов'),
    #     (11, 'Medassitance'),
    #     (12, 'Прайскурация/расчеты'),
    #     (13, 'КЛИНИЦИСТ ОЦЕНКА'),
    #     (14, 'Настройка мкб-10'),
    #     (15, 'Настройка мкб-10 ЛПУ'),
    #     (16, 'Отчет'),
    #     (17, 'Админ страховой компании'),
    #     (18, 'Админ больницы'),
    # )
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=1)
    address = models.CharField(max_length=180, null=True, blank=True)
    phone_number = models.CharField(max_length=180, null=True, blank=True)
    iin = models.CharField(max_length=180, null=True, blank=True)
    insurance = models.ForeignKey(
        Insurance, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def full_name(self):
        return self.last_name + ' ' + self.first_name