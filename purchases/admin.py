from django.contrib import admin
from .models import (
    PurchaseStatus,
    Provider,
    Purchase,
    PurchaseItem,
)

admin.site.register(PurchaseStatus)
admin.site.register(Provider)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
