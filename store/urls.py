from django.urls import path
from . import views
from .views import (
    IndexView,
    ProductListView,
    CategoryProductsView,
    DiscountedProductsView,
    ProductDetailView,
    ProductCreateView
)

app_name = 'store'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('category/<int:category_pk>/', CategoryProductsView.as_view(), name='category_products'),
    path('discounted/', DiscountedProductsView.as_view(), name='discounted_products'),
    path('products/<int:product_pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]