from rest_framework import serializers
from .models import ExaminationAppointment

class ExaminationAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationAppointment
        fields = '__all__'