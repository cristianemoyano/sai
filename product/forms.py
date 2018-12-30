from django import forms

from .models import (
    Product,
    ProductCategory,
)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'reference_code',
            'import_code',
            'description',
            'stock',
            'min_amount',
            'product_store',
            'product_category',
            'product_type',
            'product_status',
            'image_url'
        ]

class ProductCategoryForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = [
            'name',
            'code',
            'description',
        ]
