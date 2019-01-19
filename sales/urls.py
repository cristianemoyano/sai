from django.urls import path, include
from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerAPIView)

urlpatterns = [
    # Order
    path('', csrf_exempt(views.OrderList.as_view()), name='order_list'),
    path('view/<int:pk>', views.OrderView.as_view(), name='order_view'),
    path('new', csrf_exempt(views.OrderCreate.as_view()), name='order_new'),
    path('view/<int:pk>', views.OrderView.as_view(), name='order_view'),
    path('edit/<int:pk>', views.OrderUpdate.as_view(), name='order_edit'),
    path('delete/<int:pk>', views.OrderDelete.as_view(), name='order_delete'),
    path('pdv', csrf_exempt(views.OrderSale.as_view()), name='order_pdv'),
    path('ticket/<int:pk>', views.order_ticket, name='order_ticket'),
    # OrderItem
    path('item', views.OrderItemList.as_view(), name='order_item_list'),
    path('item/view/<int:pk>', views.OrderItemView.as_view(), name='order_item_view'),
    path('item/new', csrf_exempt(views.OrderItemCreate.as_view()), name='order_item_new'),
    path('item/view/<int:pk>', views.OrderItemView.as_view(), name='order_item_view'),
    path('item/edit/<int:pk>', views.OrderItemUpdate.as_view(), name='order_item_edit'),
    path('item/delete/<int:pk>', views.OrderItemDelete.as_view(), name='order_item_delete'),
    # Customer
    path('customer', views.CustomerList.as_view(), name='customer_list'),
    path('customer/view/<int:pk>', views.CustomerView.as_view(), name='customer_view'),
    path('customer/new', views.CustomerCreate.as_view(), name='customer_new'),
    path('customer/view/<int:pk>', views.CustomerView.as_view(), name='customer_view'),
    path('customer/edit/<int:pk>', views.CustomerUpdate.as_view(), name='customer_edit'),
    path('customer/delete/<int:pk>', views.CustomerDelete.as_view(), name='customer_delete'),


    # API
    path('api/', include(router.urls)),
]