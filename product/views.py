from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import (
    ProductForm,
    ProductCategoryForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Product,
    ProductCategory,
)


def dashboard(request):
    return render(request, 'product/dashboard.html', {})

# Product CRUD

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

# END Product CRUD

# ProductCategory CRUD

class ProductCategoryList(ListView):
    model = ProductCategory


class ProductCategoryView(DetailView):
    model = ProductCategory


class ProductCategoryCreate(CreateView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')
    form_class = ProductCategoryForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductCategoryUpdate(UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')
    form_class = ProductCategoryForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductCategoryDelete(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')

# END ProductCategory CRUD