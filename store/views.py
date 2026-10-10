from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Product, Category


def product_list(request):
    # ხელმისაწვდომი პროდუქტები დალაგებული ფასის ზრდადობით
    products = Product.objects.filter(is_available=True).order_by('price')

    # კატეგორიები, სადაც მინიმუმ 1 პროდუქტი მაინც არის (+ annotate პროდუქტების რაოდენობისთვის)
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/product_list.html', context)


def products_by_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    products = Product.objects.filter(category=category, is_available=True).order_by('price')

    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


def discounted_products(request):
    # მხოლოდ ფასდაკლებული პროდუქტები
    products = Product.objects.filter(is_available=True, has_discount=True).order_by('price')
    context = {
        'products': products
    }
    return render(request, 'store/discounted_products.html', context)


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    return render(request, 'store/product_detail.html', {'product': product})