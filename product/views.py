from django.shortcuts import render
from search_views.search import SearchListView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .resources import ProductResource
from .forms import (
    ProductForm,
    ProductSearchForm,
    ProductFilter,
    ProductCategoryForm,
    ProductStoreForm,
    PriceForm,
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    Product,
    ProductCategory,
    ProductStore,
    Price,
)
from purchases.models import (
    Provider,
    Purchase,
)
from sales.models import (
    Customer,
    Order,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from main.auth import GroupRequiredMixin


@login_required
def dashboard(request):
    products = Product.objects.all().count()
    providers = Provider.objects.all().count()
    customers = Customer.objects.all().count()
    purchases = Purchase.objects.all().count()
    orders = Order.objects.all().count()
    orders_sum = Order.objects.aggregate(Sum('paid_amount'))
    purchases_sum = Purchase.objects.aggregate(Sum('paid_amount'))

    purchases_amount = purchases_sum.get('paid_amount__sum')
    orders_amount = orders_sum.get('paid_amount__sum')

    if not purchases_amount:
        purchases_amount = 0
    if not orders_amount:
        orders_amount = 0

    context = {
        'products': products,
        'providers': providers,
        'customers': customers,
        'purchases': purchases,
        'orders': orders,
        'orders_amount': orders_amount,
        'purchases_amount': purchases_amount
    }

    return render(request, 'product/dashboard.html', context)

# Product CRUD


class ProductList(LoginRequiredMixin, SearchListView):
    model = Product
    paginate_by = 10
    template_name = "product/product_list.html"

    # additional configuration for SearchListView
    form_class = ProductSearchForm
    filter_class = ProductFilter


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


def product_import_file(request):
    success_url = 'product/product_import.html'
    product_fields = [
        'id',
        'created',
        'modified',
        'user',
        'name',
        'reference_code',
        'import_code',
        'description',
        'stock',
        'min_amount',
        'product_store',
        'product_category',
        'product_type',
        'product_status',
        'image_url'
    ]
    context = {}
    if request.method == 'POST':
        try:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith('.csv'):
                context['error'] = 'Formato no permitido. Sólo se permiten .CSV'
                return render(request, success_url, context)
            # if file is too large, return
            if csv_file.multiple_chunks():
                context['error'] = 'Archivo demasiado grande.'
                return render(request, success_url, context)

            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\r\n")
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                i = 0
                for field in product_fields:
                    if len(product_fields) == len(fields):
                        data_dict[field] = fields[i]
                        i += 1

                try:
                    form = ProductForm(data_dict)
                    form.instance.user_id = request.user.id
                    if form.is_valid():
                        form.save()
                except Exception as e:
                    context['error'] = 'Error inesperado: {e}'.format(e=e)
                    return render(request, success_url, context)
            context['message'] = 'Productos creados correctamente.'
        except Exception as e:
            context['error'] = 'Error inesperado: {e}'.format(e=e)
            return render(request, success_url, context)

    return render(request, success_url, context)


def product_export_csv(request):
    product_resource = ProductResource()
    dataset = product_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="producto.csv"'
    return response


def product_export_excel(request):
    product_resource = ProductResource()
    dataset = product_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producto.xls"'
    return response

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

# Price CRUD


class PriceList(LoginRequiredMixin, ListView):
    model = Price
    paginate_by = 10


class PriceView(DetailView):
    model = Price


class PriceCreate(LoginRequiredMixin, CreateView):
    model = Price
    success_url = reverse_lazy('product_price_list')
    form_class = PriceForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class PriceUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Price
    success_url = reverse_lazy('product_price_list')
    form_class = PriceForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class PriceDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Price
    success_url = reverse_lazy('product_price_list')

# END Price CRUD
