from .models import (
    Product,
)
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'reference_code',
            'stock',
            'name',
            'list_price',
        )
