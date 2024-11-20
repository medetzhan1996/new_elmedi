from rest_framework import serializers
from ..models import Customer


# Сериализатор направления
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'surname', 'iin', 'full_name']
