from rest_framework import serializers

from contract_management.models import Package
from promedicine.models import ExaminationAppointment, ExaminationResult
from directory.models import ICD

class ExaminationAppointmentSerializer(serializers.ModelSerializer):
    service_title = serializers.SerializerMethodField()

    class Meta:
        model = ExaminationAppointment
        fields = [
            'id',
            'professional_examination',
            'service_title',
            'doctor_code',
            'date_time',
            'status'
        ]

    def get_service_title(self, obj):
        return obj.service.title


class ExaminationResultListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExaminationResult
        fields = [
            'examination_appointment',
            'icd',
            'conclusion',
            'recommendations'
        ]

class PackageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = [
            'title',
            'description',
            'limit_type'
        ]




# Сериализатор направления
class ExaminationResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExaminationResult
        fields = ['examination_appointment', 'icd', 'conclusion', 'recommendations']


# from rest_framework.exceptions import NotFound
# # Сериализатор направления
# class ExaminationResultSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ExaminationResult
#         fields = ['examination_appointment', 'icd', 'conclusion', 'recommendations']
#
#     def create(self, validated_data):
#         # Получаем строковые представления из данных
#         examination_appointment_str = validated_data.pop('examination_appointment', None)
#         icd_str = validated_data.pop('icd', None)
#
#         # Ищем соответствующие объекты моделей
#         try:
#             examination_appointment_obj = ExaminationAppointment.objects.get(service__title=examination_appointment_str)
#         except ExaminationAppointment.DoesNotExist:
#             raise NotFound(detail="ExaminationAppointment not found")
#
#         try:
#             icd_obj = ICD.objects.get(code=icd_str)
#         except ICD.DoesNotExist:
#             raise NotFound(detail="ICD not found")
#
#         # Создаем и возвращаем объект модели ExaminationResult
#         examination_result = ExaminationResult.objects.create(examination_appointment=examination_appointment_obj, icd=icd_obj, **validated_data)
#         return examination_result
