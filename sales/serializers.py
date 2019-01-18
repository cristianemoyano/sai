from .models import (
    Customer,
)
from rest_framework import serializers


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'pk',
            'identifier_number',
            'first_name',
            'last_name',
            'company',
            'street_address_1',
            'mobile_number',
        )
