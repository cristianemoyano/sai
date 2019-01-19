from main.models import TimeStampedModel
from django.conf import settings
from django.db import models
from decimal import Decimal


class ProductStore(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductCategory(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductType(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    parameter = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductStatus(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    reference_code = models.CharField(max_length=200, unique=True, blank=False, null=True)
    import_code = models.CharField(max_length=200)
    description = models.TextField()
    stock = models.IntegerField()
    min_amount = models.IntegerField()
    product_store = models.ForeignKey(ProductStore, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def list_price(self):
        price = Price.objects.filter(product=self.id).latest('list_price')
        return price.list_price

    @property
    def cost_price(self):
        price = Price.objects.filter(product=self.id).latest('list_price')
        return price.cost_price

    @property
    def price_a(self):
        price = Price.objects.filter(product=self.id).latest('list_price')
        return price.price_a

    @property
    def price_b(self):
        price = Price.objects.filter(product=self.id).latest('list_price')
        return price.price_b

    @property
    def price_c(self):
        price = Price.objects.filter(product=self.id).latest('list_price')
        return price.price_c
    
    @property
    def stock_status(self):
        return _get_product_stock_status(self.id)
    
    @property
    def profit_list_price(self):
        list_price = Decimal(str(self.list_price))
        cost_price = Decimal(str(self.cost_price))
        percent = Decimal('100')
        profit = ((list_price-cost_price)/ list_price) * percent
        return round(profit,2)

def _get_product_stock_status(product_id):
    product =  Product.objects.get(id=product_id)
    if product:
        stock = product.stock
        min_amount = product.min_amount
        distance = stock-min_amount
        if stock <= 0:
            return {
                'label': 'En Peligro',
                'class': 'danger'
            }
        if stock <= min_amount and stock > 0:
            return {
                'label': 'En Alerta',
                'class': 'warning'
            }
        if distance > 0 and distance <= 3:
            return {
                'label': 'Próximo a reponer',
                'class': 'primary'
            }
        if distance > 0 and distance > 3:
            return {
                'label': 'Saludable',
                'class': 'success'
            }


class Currency(TimeStampedModel):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Price(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2)
    list_price = models.DecimalField(max_digits=20, decimal_places=2)
    price_a = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_b = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_c = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
