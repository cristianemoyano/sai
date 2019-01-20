from django.conf import settings
from main.models import TimeStampedModel
from django.db import models
from product.models import (
    Product,
    Currency,
)


class OrderStatus(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class PaymentMethod(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Country(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Region(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Customer(TimeStampedModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    identifier_number = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=200)
    work_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    web_url = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.IntegerField(blank=True, null=True)
    street_address_1 = models.TextField(blank=True, null=True)
    street_address_2 = models.TextField(blank=True, null=True)
    address_note = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Order(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=200, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    additional_notes = models.TextField(blank=True, null=True)
    gross_amount = models.DecimalField(max_digits=20, decimal_places=2)
    tax = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    shipping = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_address = models.TextField(blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    invoice_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '#' + str(self.id)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()
    taxes = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.product.name
