from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import (
    OrderForm,
    CustomerForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Order,
    Customer,
)

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
