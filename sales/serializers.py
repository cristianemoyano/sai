from .models import (
    Customer,
    City,
)
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name')

class CustomerSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    region = serializers.ReadOnlyField(source='region.name')
    country = serializers.ReadOnlyField(source='country.name')
    
    class Meta:
        model = Customer
        fields = (
            'pk',
            'identifier_number',
            'first_name',
            'last_name',
            'company',
            'street_address_1',
            'street_address_2',
            'mobile_number',
            'work_number',
            'city',
            'region',
            'country',
            'zip_code',
        )

