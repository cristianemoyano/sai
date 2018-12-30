from django.contrib import admin
from .models import (
    OrderStatus,
    PaymentMethod,
    Country,
    Region,
    City,
    Customer,
    Order,
    OrderItem,
)

admin.site.register(OrderStatus)
admin.site.register(PaymentMethod)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
