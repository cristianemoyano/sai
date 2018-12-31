from django.urls import path
from . import views

urlpatterns = [
    # Order
    path('', views.OrderList.as_view(), name='order_list'),
    path('view/<int:pk>', views.OrderView.as_view(), name='order_view'),
    path('new', views.OrderCreate.as_view(), name='order_new'),
    path('view/<int:pk>', views.OrderView.as_view(), name='order_view'),
    path('edit/<int:pk>', views.OrderUpdate.as_view(), name='order_edit'),
    path('delete/<int:pk>', views.OrderDelete.as_view(), name='order_delete'),
    # Customer
    path('customer', views.CustomerList.as_view(), name='customer_list'),
    path('customer/view/<int:pk>', views.CustomerView.as_view(), name='customer_view'),
    path('customer/new', views.CustomerCreate.as_view(), name='customer_new'),
    path('customer/view/<int:pk>', views.CustomerView.as_view(), name='customer_view'),
    path('customer/edit/<int:pk>', views.CustomerUpdate.as_view(), name='customer_edit'),
    path('customer/delete/<int:pk>', views.CustomerDelete.as_view(), name='customer_delete'),
]