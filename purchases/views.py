from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import (
    PurchaseForm,
    ProviderForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Purchase,
    Provider,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from main.auth import GroupRequiredMixin

# Purchase CRUD

class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    paginate_by = 10


class PurchaseView(LoginRequiredMixin, DetailView):
    model = Purchase


class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    success_url = reverse_lazy('purchase_list')
    form_class = PurchaseForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class PurchaseUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Purchase
    success_url = reverse_lazy('purchase_list')
    form_class = PurchaseForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class PurchaseDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Purchase
    success_url = reverse_lazy('purchase_list')

# END Purchase CRUD

# Provider CRUD

class ProviderList(LoginRequiredMixin, ListView):
    model = Provider
    paginate_by = 10


class ProviderView(LoginRequiredMixin, DetailView):
    model = Provider


class ProviderCreate(LoginRequiredMixin, CreateView):
    model = Provider
    success_url = reverse_lazy('Provider_list')
    form_class = ProviderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProviderUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Provider
    success_url = reverse_lazy('Provider_list')
    form_class = ProviderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProviderDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Provider
    success_url = reverse_lazy('Provider_list')

# END Provider CRUD
