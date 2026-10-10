from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_pk>/', views.products_by_category, name='category_products'),
    path('discounted/', views.discounted_products, name='discounted_products'),
    path('products/<int:product_pk>/', views.product_detail, name='product_detail'),
]