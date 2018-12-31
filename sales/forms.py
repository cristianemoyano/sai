from django import forms

from .models import (
    Order,
    Customer,
)

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer',
            'additional_notes',
            'gross_amount',
            'tax',
            'discount',
            'shipping',
            'paid_amount',
            'status',
            'payment_method',
            'currency',
            'invoice_url',
        ]

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'mobile_number',
            'work_number',
            'email',
            'company',
            'web_url',
            'country',
            'region',
            'city',
            'zip_code',
            'street_address_1',
            'street_address_2',
            'address_note',
            'additional_notes',
        ]
