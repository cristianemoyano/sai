from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .forms import (
    OrderForm,
    CustomerForm,
    OrderItemForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Order,
    OrderItem,
    Customer,
    OrderStatus,
    PaymentMethod,
    Currency,
)
from product.models import (
    Product,
)
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from main.auth import GroupRequiredMixin

# Order CRUD

class OrderList(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10


class OrderView(LoginRequiredMixin, DetailView):
    model = Order


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    success_url = reverse_lazy('order_list')
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class OrderUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Order
    success_url = reverse_lazy('order_list')
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class OrderDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')

# END Order CRUD

# Customer CRUD

class CustomerList(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 10


class CustomerView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    success_url = reverse_lazy('customer_list')
    form_class = CustomerForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class CustomerUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    success_url = reverse_lazy('customer_list')
    form_class = CustomerForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class CustomerDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')

# END Customer CRUD

# OrderItem CRUD

class OrderItemList(LoginRequiredMixin, ListView):
    model = OrderItem
    paginate_by = 10


class OrderItemView(LoginRequiredMixin, DetailView):
    model = OrderItem


def get_dynamic_fields(request_fields, object_name, object_fields):
    crsftoken = 'csrfmiddlewaretoken'
    dynamic_fields = {
            crsftoken: '',
            object_name: object_fields,
        }
    for key, value in request_fields.items():
        keys = key.split('[')
        if not crsftoken in keys:
            correlation_id = keys[2].split(']')[0]
            field_name = keys[3].split(']')[0]
            dynamic_fields[object_name][field_name].append(
                {'value': value, 'correlation_id': correlation_id}
            )
            if not correlation_id in dynamic_fields[object_name]['correlation_ids']:
                dynamic_fields[object_name]['correlation_ids'].append(correlation_id)
        else:
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
        if key in object_field_list:
            object_items[key] = value
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
        'status',
        'payment_method',
        'currency',
        'invoice_url',
    ]
    order_items = get_object_items(request_fields, order_fields_list)
    order_items['customer'] = Customer.objects.get(id=order_items.get('customer'))
    order_items['status'] = OrderStatus.objects.get(id=order_items.get('status'))
    order_items['payment_method'] = PaymentMethod.objects.get(id=order_items.get('payment_method'))
    order_items['currency'] = Currency.objects.get(id=order_items.get('currency'))
    order_items['user'] = User.objects.get(id=user_id)
    order = Order.objects.create(**order_items)
    order.save()
    return order.id

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
    for order_item in order_item_schema:
        del order_item['id']
        order_item['order_id'] = create_order_and_get_order_id(request_fields, user_id)
        order_item['product'] = Product.objects.get(id=order_item.get('product'))
        objects_to_create.append(OrderItem(**order_item))
    OrderItem.objects.bulk_create(objects_to_create)

class OrderItemCreate(LoginRequiredMixin, CreateView):
    model = OrderItem
    success_url = reverse_lazy('order_item_list')
    form_class = OrderItemForm


    def post(self, request, *args, **kwargs):
        request_fields = request.POST.dict()
        create_order_items(request_fields, request.user.id)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(OrderItemCreate, self).get_context_data(**kwargs)
        extra_context = {
            'order_form': OrderForm()
        }
        context.update(extra_context)
        return context


class OrderItemUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = OrderItem
    success_url = reverse_lazy('order_item_list')
    form_class = OrderItemForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class OrderItemDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = OrderItem
    success_url = reverse_lazy('order_item_list')

# END OrderItem CRUD