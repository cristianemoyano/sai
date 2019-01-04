from django import forms

from .models import (
    Purchase,
    Provider,
    PurchaseItem,
)
from search_views.filters import BaseFilter


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


class PurchaseFilter(BaseFilter):
    search_fields = {
        'search_text': ['description', 'reference_code', 'import_code', 'name'],
    }


class PurchaseSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar...',
            'class': 'form-control',
        })
    )


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
