from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.ProductList.as_view(), name='product_list'),
    path('view/<int:pk>', views.ProductView.as_view(), name='product_view'),
    path('new', views.ProductCreate.as_view(), name='product_new'),
    path('view/<int:pk>', views.ProductView.as_view(), name='product_view'),
    path('edit/<int:pk>', views.ProductUpdate.as_view(), name='product_edit'),
    path('delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
]
