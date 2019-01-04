from django.urls import path
from . import views

urlpatterns = [
    # Product
    path('', views.ProductList.as_view(), name='product_list'),
    path('view/<int:pk>', views.ProductView.as_view(), name='product_view'),
    path('new', views.ProductCreate.as_view(), name='product_new'),
    path('view/<int:pk>', views.ProductView.as_view(), name='product_view'),
    path('edit/<int:pk>', views.ProductUpdate.as_view(), name='product_edit'),
    path('delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
    path('export_csv', views.product_export_csv, name='product_export_csv'),
    path('export_excel', views.product_export_excel, name='product_export_excel'),
    path('import_file', views.product_import_file, name='product_import_file'),
    # ProductCategory
    path('category', views.ProductCategoryList.as_view(), name='product_category_list'),
    path('category/view/<int:pk>', views.ProductCategoryView.as_view(), name='product_category_view'),
    path('category/new', views.ProductCategoryCreate.as_view(), name='product_category_new'),
    path('category/view/<int:pk>', views.ProductCategoryView.as_view(), name='product_category_view'),
    path('category/edit/<int:pk>', views.ProductCategoryUpdate.as_view(), name='product_category_edit'),
    path('category/delete/<int:pk>', views.ProductCategoryDelete.as_view(), name='product_category_delete'),
    # ProductStore
    path('store', views.ProductStoreList.as_view(), name='product_store_list'),
    path('store/view/<int:pk>', views.ProductStoreView.as_view(), name='product_store_view'),
    path('store/new', views.ProductStoreCreate.as_view(), name='product_store_new'),
    path('store/view/<int:pk>', views.ProductStoreView.as_view(), name='product_store_view'),
    path('store/edit/<int:pk>', views.ProductStoreUpdate.as_view(), name='product_store_edit'),
    path('store/delete/<int:pk>', views.ProductStoreDelete.as_view(), name='product_store_delete'),
    # Price
    path('price', views.PriceList.as_view(), name='product_price_list'),
    path('price/view/<int:pk>', views.PriceView.as_view(), name='product_price_view'),
    path('price/new', views.PriceCreate.as_view(), name='product_price_new'),
    path('price/view/<int:pk>', views.PriceView.as_view(), name='product_price_view'),
    path('price/edit/<int:pk>', views.PriceUpdate.as_view(), name='product_price_edit'),
    path('price/delete/<int:pk>', views.PriceDelete.as_view(), name='product_price_delete'),
]
