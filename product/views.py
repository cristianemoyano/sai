from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import (
    ProductForm,
    ProductCategoryForm,
    ProductStoreForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Product,
    ProductCategory,
    ProductStore,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission

class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            permissions = Permission.objects.filter(user=request.user)
            if not request.user.has_perm(permissions):
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):
    return render(request, 'product/dashboard.html', {})

# Product CRUD

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10


class ProductView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('product_list')
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('product_list')
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

# END Product CRUD

# ProductCategory CRUD

class ProductCategoryList(LoginRequiredMixin, ListView):
    model = ProductCategory
    paginate_by = 10


class ProductCategoryView(DetailView):
    model = ProductCategory


class ProductCategoryCreate(LoginRequiredMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')
    form_class = ProductCategoryForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductCategoryUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')
    form_class = ProductCategoryForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductCategoryDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_list')

# END ProductCategory CRUD

# ProductStore CRUD

class ProductStoreList(LoginRequiredMixin, ListView):
    model = ProductStore
    paginate_by = 10


class ProductStoreView(DetailView):
    model = ProductStore


class ProductStoreCreate(LoginRequiredMixin, CreateView):
    model = ProductStore
    success_url = reverse_lazy('product_store_list')
    form_class = ProductStoreForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductStoreUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = ProductStore
    success_url = reverse_lazy('product_store_list')
    form_class = ProductStoreForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProductStoreDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ProductStore
    success_url = reverse_lazy('product_store_list')

# END ProductStore CRUD