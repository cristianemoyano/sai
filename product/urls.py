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
    # ProductCategory
    path('category', views.ProductCategoryList.as_view(), name='product_category_list'),
    path('category/view/<int:pk>', views.ProductCategoryView.as_view(), name='product_category_view'),
    path('category/new', views.ProductCategoryCreate.as_view(), name='product_category_new'),
    path('category/view/<int:pk>', views.ProductCategoryView.as_view(), name='product_category_view'),
    path('category/edit/<int:pk>', views.ProductCategoryUpdate.as_view(), name='product_category_edit'),
    path('category/delete/<int:pk>', views.ProductCategoryDelete.as_view(), name='product_category_delete'),
]
