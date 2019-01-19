from django.http import HttpResponseRedirect
from search_views.search import SearchListView
from django.views.generic import ListView, DetailView
from .forms import (
    PurchaseForm,
    ProviderForm,
    PurchaseItemForm,
    ProviderSearchForm,
    ProviderFilter,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Purchase,
    PurchaseItem,
    Provider,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from main.auth import GroupRequiredMixin
from main.utils import create_purchase_items

# Purchase CRUD


class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase


class PurchaseView(LoginRequiredMixin, DetailView):
    model = Purchase

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        purchase_id = context.get('object').id
        purchase_items = PurchaseItem.objects.filter(purchase_id=purchase_id)
        extra_context = {
            'purchase_items': purchase_items
        }
        context.update(extra_context)
        return context


class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    success_url = reverse_lazy('purchase_list')
    form_class = PurchaseItemForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        request_fields = request.POST.dict()
        create_purchase_items(request_fields, request.user.id)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(PurchaseCreate, self).get_context_data(**kwargs)
        extra_context = {
            'purchase_form': PurchaseForm()
        }
        context.update(extra_context)
        return context


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


class ProviderList(LoginRequiredMixin, SearchListView):
    model = Provider
    template_name = 'purchases/provider_list.html'

    # additional configuration for SearchListView
    form_class = ProviderSearchForm
    filter_class = ProviderFilter


class ProviderView(LoginRequiredMixin, DetailView):
    model = Provider


class ProviderCreate(LoginRequiredMixin, CreateView):
    model = Provider
    success_url = reverse_lazy('provider_list')
    form_class = ProviderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProviderUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Provider
    success_url = reverse_lazy('provider_list')
    form_class = ProviderForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProviderDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Provider
    success_url = reverse_lazy('provider_list')

# END Provider CRUD
