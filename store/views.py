from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Product, Category
from .forms import ProductForm

def index(request):
    return render(request, 'store/index.html')

def product_list(request):
    # ხელმისაწვდომი პროდუქტები დალაგებული ფასის ზრდადობით
    products = Product.objects.filter(is_available=True).order_by('price')

    # კატეგორიები, სადაც მინიმუმ 1 პროდუქტი მაინც არის
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

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:product_list')  # გასწორდა
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Create'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:product_detail', product_pk=product.pk)  # გასწორდა
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Update'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:product_list')  # გასწორდა
    return render(request, 'store/product_confirm_delete.html', {'product': product})