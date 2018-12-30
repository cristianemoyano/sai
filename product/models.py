from django.conf import settings
from django.db import models
from django.utils import timezone


class ProductStore(models.Model):
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


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    parameter = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    parameter = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class ProductStatus(models.Model):
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


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    reference_code = models.CharField(max_length=200)
    import_code = models.CharField(max_length=200)
    description = models.TextField()
    stock = models.IntegerField()
    min_amount = models.IntegerField()
    product_store = models.ForeignKey(ProductStore, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2)
    list_price = models.DecimalField(max_digits=20, decimal_places=2)
    price_a = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_b = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_c = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.product.name
