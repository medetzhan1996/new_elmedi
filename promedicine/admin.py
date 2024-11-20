from django.contrib import admin
from .models import ProfessionalExamination, ExaminationAppointment, ExaminationResult, Conclusion, SpecialityService, HazardReference

admin.site.register(ProfessionalExamination)
admin.site.register(ExaminationAppointment)
admin.site.register(ExaminationResult)
admin.site.register(Conclusion)
admin.site.register(SpecialityService)
admin.site.register(HazardReference)
