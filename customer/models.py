from django.db import models


# Клиент
class Customer(models.Model):
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    surname = models.CharField(max_length=180, blank=True, null=True)
    national = models.CharField(max_length=180, blank=True, null=True)
    address = models.CharField(max_length=180, blank=True, null=True)
    place_work = models.CharField(max_length=180, blank=True, null=True)
    telephone_number = models.CharField(max_length=180, blank=True, null=True)
    profession = models.CharField(max_length=180, blank=True, null=True)
    iin = models.CharField(max_length=13, unique=True)
    signature = models.FileField(upload_to='signatures/', blank=True, null=True)

    @property
    def full_name(self):
        return "{} {}".format(
            self.last_name, self.first_name)

    def __str__(self):
        return "ИИН: {}, ФИО: {} {}".format(
            self.iin, self.last_name, self.first_name)
