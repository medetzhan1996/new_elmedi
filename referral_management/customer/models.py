from django.db import models


# Клиент
class Customer(models.Model):
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    surname = models.CharField(max_length=180)
    national = models.CharField(max_length=180)
    address = models.CharField(max_length=180)
    place_work = models.CharField(max_length=180)
    telephone_number = models.CharField(max_length=180)
    profession = models.CharField(max_length=180)
    iin = models.CharField(max_length=13, unique=True)

    @property
    def full_name(self):
        return "{} {} {}".format(
            self.last_name, self.first_name, self.surname)

    def __str__(self):
        return "ИИН: {}, ФИО: {} {}".format(
            self.iin, self.last_name, self.first_name)
