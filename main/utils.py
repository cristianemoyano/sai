from product.models import (
    Product,
    ProductStatus,
)
from django.contrib.auth.models import User
from sales.models import (
    Order,
    OrderItem,
    Customer,
    OrderStatus,
    PaymentMethod,
    Currency,
)


def get_dynamic_fields(request_fields, object_name, object_fields):
    crsftoken = 'csrfmiddlewaretoken'
    excempt_fields_list = [
        crsftoken,
        'customer',
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
    dynamic_fields = {
        crsftoken: '',
        object_name: object_fields,
    }
    for key, value in request_fields.items():
        field_name = key.split('[')[2].split(']')[0]
        if field_name not in excempt_fields_list:
            field_name = key.split('[')[3].split(']')[0]
            correlation_id = key.split('[')[2].split(']')[0]
            dynamic_fields[object_name][field_name].append(
                {'value': value, 'correlation_id': correlation_id}
            )
            if correlation_id not in dynamic_fields[object_name]['correlation_ids']:
                dynamic_fields[object_name]['correlation_ids'].append(correlation_id)
        elif crsftoken == field_name:
            dynamic_fields[crsftoken] = value
    return dynamic_fields


def get_value_by_id(items, id):
    for item in items:
        if item.get('correlation_id') == id:
            return item.get('value')


def get_dynamic_items(request_fields):
    dynamic_items = {}
    for key, value in request_fields.items():
        if 'dynamic_form[dynamic_form]' in key:
            dynamic_items[key] = value
    return dynamic_items


def get_object_items(request_fields, object_field_list):
    object_items = {}
    for key, value in request_fields.items():
        field_name = key.split('[')[2].split(']')[0]
        if field_name in object_field_list:
            object_items[field_name] = value
    return object_items


def build_schema_order_item(order_items_dict, object_fields):
    order_item_schema = []
    for item_id in order_items_dict.get('correlation_ids'):
        order_item = {}
        order_item['id'] = item_id
        for field in object_fields:
            order_item[field] = get_value_by_id(order_items_dict.get(field), item_id)
        order_item_schema.append(order_item)
    return order_item_schema


def create_order_and_get_order_id(request_fields, user_id):
    order_fields_list = [
        'customer',
        'additional_notes',
        'gross_amount',
        'tax',
        'discount',
        'shipping',
        'paid_amount',
        'payment_method',
        'currency',
        'invoice_url',
    ]
    order_items = get_object_items(request_fields, order_fields_list)
    order_items['customer'] = Customer.objects.get(id=order_items.get('customer'))
    order_items['status'] = OrderStatus.objects.get(code='PAID')
    order_items['payment_method'] = PaymentMethod.objects.get(id=order_items.get('payment_method'))
    order_items['currency'] = Currency.objects.get(id=order_items.get('currency'))
    order_items['user'] = User.objects.get(id=user_id)
    order = Order.objects.create(**order_items)
    order.save()
    return order.id


def manage_stock_product(id, quantity):
    product = Product.objects.get(id=id)
    new_stock = product.stock - int(quantity)
    product.stock = new_stock
    if (new_stock <= 0):
        product.product_status = ProductStatus.objects.get(code='not_available')
    product.save()
    return product


def create_order_items(request_fields, user_id):
    dynamic_items = get_dynamic_items(request_fields)
    order_item_fields_dict = {
        'correlation_ids': [],
        'product': [],
        'unit_price': [],
        'quantity': [],
        'amount': [],
    }
    order_item_fields_list = ['product', 'unit_price', 'quantity', 'amount']
    dynamic_fields = get_dynamic_fields(dynamic_items, 'order_items', order_item_fields_dict)
    order_item_schema = build_schema_order_item(dynamic_fields.get('order_items'), order_item_fields_list)

    objects_to_create = []
    order_id = create_order_and_get_order_id(request_fields, user_id)
    for order_item in order_item_schema:
        del order_item['id']
        order_item['order_id'] = order_id
        product_id = order_item.get('product')
        quantity = order_item.get('quantity')
        order_item['product'] = manage_stock_product(product_id, quantity)
        objects_to_create.append(OrderItem(**order_item))
    OrderItem.objects.bulk_create(objects_to_create)
