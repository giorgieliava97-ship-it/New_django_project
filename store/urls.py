from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),      path('category/<int:category_pk>/', views.products_by_category, name='category_products'),
    path('discounted/', views.discounted_products, name='discounted_products'),
    path('products/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]