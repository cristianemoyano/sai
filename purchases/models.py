from django.conf import settings
from django.db import models
from django.utils import timezone
from product.models import (
    Product,
    Currency,
)
from sales.models import (
    Country,
    Region,
    City,
    PaymentMethod,
)


class PurchaseStatus(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Provider(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
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
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    additional_notes = models.TextField(blank=True, null=True)
    gross_amount = models.DecimalField(max_digits=20, decimal_places=2)
    tax = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    shipping = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.ForeignKey(PurchaseStatus, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    invoice_url = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return '#' + str(self.id)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.product.name
