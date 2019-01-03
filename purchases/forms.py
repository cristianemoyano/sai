from django import forms

from .models import (
    Purchase,
    Provider,
    PurchaseItem,
)


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = [
            'provider',
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


class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseItem
        fields = [
            'product',
            'unit_price',
            'quantity',
            'amount',
        ]


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
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
