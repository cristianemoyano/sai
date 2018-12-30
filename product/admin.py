from django.contrib import admin
from .models import (
    ProductStore,
    ProductCategory,
    ProductType,
    ProductStatus,
    Product,
    Currency,
    Price,
)

admin.site.register(ProductStore)
admin.site.register(ProductCategory)
admin.site.register(ProductType)
admin.site.register(ProductStatus)
admin.site.register(Product)
admin.site.register(Currency)
admin.site.register(Price)
