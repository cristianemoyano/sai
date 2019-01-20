import json
from django.http import HttpResponse, HttpResponseRedirect
from search_views.search import SearchListView
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.core import serializers
from django.db import transaction
from .forms import (
    OrderForm,
    CustomerForm,
    CustomerSearchForm,
    CustomerFilter,
    OrderItemForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Order,
    OrderItem,
    Customer,
    PaymentMethod,
    OrderStatus,
)
from .serializers import CustomerSerializer
from rest_framework import viewsets


from django.contrib.auth.mixins import LoginRequiredMixin
from main.auth import GroupRequiredMixin
from main.utils import create_order_items, manage_stock_product

from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal
from product.models import (
    Product,
    Currency,
)
# Order CRUD


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    ordering = ['-created']


class OrderView(LoginRequiredMixin, DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        order_id = context.get('object').id
        order_items = OrderItem.objects.filter(order_id=order_id)
        extra_context = {
            'order_items': order_items
        }
        context.update(extra_context)
        return context


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    success_url = reverse_lazy('order_list')
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

class OrderSale(LoginRequiredMixin, CreateView):
    model = Order
    success_url = reverse_lazy('order_list')
    form_class = OrderForm
    template_name = 'sales/order_sale.html'

    def get_context_data(self, **kwargs):
        context = super(OrderSale, self).get_context_data(**kwargs)
        payment_methods = PaymentMethod.objects.all().values('id', 'name')
        order_status = OrderStatus.objects.all().values('id', 'name')
        extra_context = {
            'payment_methods': payment_methods,
            'order_status': order_status,
        }
        context.update(extra_context)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            print(proceso)
            if 'serie' not in proceso:
                msg = 'Ingrese serie'
                raise Exception(msg)

            if 'number' not in proceso:
                msg = 'Ingrese numero'
                raise Exception(msg)

            if 'customer_id' not in proceso:
                msg = 'El cliente no ha sido seleccionado'
                raise Exception(msg)

            if len(proceso['order_items']) <= 0:
                msg = 'No se ha seleccionado ningun producto'
                raise Exception(msg)


            gross_amount = Decimal(proceso['gross_amount'])
            tax = Decimal(proceso['tax'])
            paid_amount = Decimal(proceso['paid_amount'])
            discount = Decimal(proceso['discount'])
            shipping = Decimal(proceso['shipping'])
            order_status_id = int(proceso['order_status'])
            payment_method_id = int(proceso['payment_method'])
            additional_notes = proceso['additional_notes']
            shipping_address = proceso['shipping_address']

            code = proceso['serie'] + '-' + proceso['number']
            order = Order(
                code=code,
                customer=Customer.objects.get(id=proceso['customer_id']),
                paid_amount=paid_amount,
                gross_amount=gross_amount,
                tax=tax,
                discount=discount,
                shipping=shipping,
                status=OrderStatus.objects.get(id=order_status_id),
                currency=Currency.objects.get(code='ARS'),
                payment_method=PaymentMethod.objects.get(id=payment_method_id),
                additional_notes=additional_notes,
                shipping_address=shipping_address,
                user=request.user,
            )
            order.save()
            print("Sale generated")
            print(order.id)
            for order_item in proceso['order_items']:
                product = Product.objects.get(id=order_item['product_id'])
                qty = Decimal(order_item['quantity'])
                price = product.list_price
                tax = Decimal('0.21')
                taxes = (price * qty) * tax
                amount = qty * price
                manage_stock_product(product.id, qty, 'SALE')
                order_item = OrderItem(
                    product=product,
                    unit_price=price,
                    quantity=qty,
                    taxes=taxes,
                    amount=amount,
                    order=order,
                )
                order_item.save()
            messages.success(
                request, 'La venta se ha realizado satisfactoriamente')
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)
        return render(request, 'sales/order_sale.html', {'form': None})


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


class CustomerList(LoginRequiredMixin, SearchListView):
    model = Customer
    template_name = 'sales/customer_list.html'

    # additional configuration for SearchListView
    form_class = CustomerSearchForm
    filter_class = CustomerFilter


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


class OrderItemView(LoginRequiredMixin, DetailView):
    model = OrderItem


class OrderItemCreate(LoginRequiredMixin, CreateView):
    model = OrderItem
    success_url = reverse_lazy('order_list')
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



# API

# Search Customer for Sale
def search_customer(request):
    id_customer = request.GET['id']
    customers = Customer.objects.filter(identifier_number__contains=id_customer)
    data = serializers.serialize(
        'json',
        customers,
        fields=(
            'identifier_number',
            'first_name',
            'last_name',
            'mobile_number',
            'street_address_1',
        )
    )
    return HttpResponse(data, content_type='application/json')

def order_ticket(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'sales/order_ticket.html', context)


class CustomerAPIView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created')
    serializer_class = CustomerSerializer
    lookup_url_kwarg = 'identifier_number'

    def get_queryset(self):
        code = self.request.query_params.get(self.lookup_url_kwarg)
        customers = Customer.objects.all().order_by('-created')
        if code:
            customers = Customer.objects.filter(
                Q(identifier_number__icontains=code) | 
                Q(first_name__icontains=code) | 
                Q(last_name__icontains=code) | 
                Q(email__icontains=code)
            )
        return customers

