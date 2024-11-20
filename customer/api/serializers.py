from rest_framework import serializers
from ..models import Customer



# Сериализатор клиента
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'iin']

