from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import ProductForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Product


def dashboard(request):
    return render(request, 'product/dashboard.html', {})


class ProductList(ListView):
    model = Product


class ProductView(DetailView):
    model = Product


class ProductCreate(CreateView):
    model = Product
    success_url = reverse_lazy('product_list')
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductUpdate(UpdateView):
    model = Product
    success_url = reverse_lazy('product_list')
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
