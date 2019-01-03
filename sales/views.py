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
)


from django.contrib.auth.mixins import LoginRequiredMixin
from main.auth import GroupRequiredMixin
from main.utils import create_order_items

# Order CRUD


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10


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
