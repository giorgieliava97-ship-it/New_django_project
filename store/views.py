from contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Category
from .forms import ProductForm

# def index(request):
#     products = Product.objects.filter(is_available=True).order_by('-id')[:8]
#     return render(request, 'store/index.html', {'products': products})

class IndexView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(is_available=True).order_by('-id')[:8]

# def product_list(request):
#     # ხელმისაწვდომი პროდუქტები დალაგებული ფასის ზრდადობით
#     products = Product.objects.filter(is_available=True).order_by('price')
#     return render(request, 'store/product_list.html', {'products': products})

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_available=True)
    ordering = ['price']


# def products_by_category(request, category_pk):
#     category = get_object_or_404(Category, pk=category_pk)
#     products = Product.objects.filter(category=category, is_available=True).order_by('price')
#     return render(request, 'store/category_products.html', {'category': category, 'products': products})

class CategoryProductsView(ListView):
    model = Product
    template_name = 'store/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        return Product.objects.filter(category=self.category, is_available=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# def discounted_products(request):
#     # მხოლოდ ფასდაკლებული პროდუქტები
#     products = Product.objects.filter(is_available=True, has_discount=True).order_by('price')
#     return render(request, 'store/discounted_products.html', {'products': products})

class DiscountedProductsView(ListView):
    model = Product
    template_name = 'store/discounted_products.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(is_available=True, has_discount=True).order_by('price')
#
# def product_detail(request, product_pk):
#     product = get_object_or_404(Product, pk=product_pk)
#     return render(request, 'store/product_detail.html', {'product': product})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_pk'

# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('store:product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'store/product_form.html', {'form': form, 'action': 'Create'})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('store:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:product_detail', product_pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Update'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})