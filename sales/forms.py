from django import forms

from .models import (
    Order,
    OrderItem,
    Customer,
)
from search_views.filters import BaseFilter


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


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'unit_price',
            'quantity',
            'amount',
        ]


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'identifier_number',
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


class CustomerFilter(BaseFilter):
    search_fields = {
        'search_text': ['first_name', 'last_name', 'company', 'email'],
    }


class CustomerSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar...',
            'class': 'form-control',
        })
    )
