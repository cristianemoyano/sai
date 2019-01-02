from django.urls import path
from . import views

urlpatterns = [
    # Purchase
    path('', views.PurchaseList.as_view(), name='purchase_list'),
    path('view/<int:pk>', views.PurchaseView.as_view(), name='purchase_view'),
    path('new', views.PurchaseCreate.as_view(), name='purchase_new'),
    path('view/<int:pk>', views.PurchaseView.as_view(), name='purchase_view'),
    path('edit/<int:pk>', views.PurchaseUpdate.as_view(), name='purchase_edit'),
    path('delete/<int:pk>', views.PurchaseDelete.as_view(), name='purchase_delete'),
    # Provider
    path('provider', views.ProviderList.as_view(), name='provider_list'),
    path('provider/view/<int:pk>', views.ProviderView.as_view(), name='provider_view'),
    path('provider/new', views.ProviderCreate.as_view(), name='provider_new'),
    path('provider/view/<int:pk>', views.ProviderView.as_view(), name='provider_view'),
    path('provider/edit/<int:pk>', views.ProviderUpdate.as_view(), name='provider_edit'),
    path('provider/delete/<int:pk>', views.ProviderDelete.as_view(), name='provider_delete'),
]
