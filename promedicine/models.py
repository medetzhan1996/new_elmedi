from django.db import models

from contract_management.models import ContractCustomer
from directory.models import Service, ICD

class SpecialityService(models.Model):
    title = models.CharField(max_length=240)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.title

class Conclusion(models.Model):
    title = models.CharField(max_length=240)

    def __str__(self):
        return self.title


class ProfessionalExamination(models.Model):
    contract_customer = models.OneToOneField(ContractCustomer, on_delete=models.CASCADE, null=True)
    plan_start_date = models.DateTimeField(null=True, blank=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=[('Planned', 'Запланирован'), ('Completed', 'Выполнен')], default='Planned')

    # def get_speciality_titles(self):
    #     speciality_titles = set()
    #     examination_appointments = self.examinationappointment_set.all()
    #
    #     for appointment in examination_appointments:
    #         services = appointment.service.specialityservice_set.values_list('title', flat=True)
    #         speciality_titles.update(services)
    #
    #     return list(speciality_titles)


class ExaminationAppointment(models.Model):
    professional_examination = models.ForeignKey(ProfessionalExamination, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    doctor_code = models.CharField(max_length=10, verbose_name='Doctor Code')
    date_time = models.DateTimeField(verbose_name='Appointment Date and Time')
    status = models.CharField(max_length=15, choices=[('Planned', 'Запланирован'), ('Completed', 'Выполнен'), ('Canceled', 'Отменен')], default='Planned')


class ExaminationResult(models.Model):
    examination_appointment = models.ForeignKey(ExaminationAppointment, on_delete=models.CASCADE)
    icd = models.ForeignKey(ICD, on_delete=models.CASCADE, null=True)
    conclusion = models.ForeignKey(Conclusion, on_delete=models.CASCADE, null=True)
    recommendations = models.TextField(verbose_name='Recommendations')

class HazardReference(models.Model):
    title = models.CharField(max_length=240, verbose_name='Название вредности')

    def __str__(self):
        return self.title
