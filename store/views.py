from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Category
from .forms import ProductForm


class IndexView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True).order_by('-id')[:8]


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_available=True)
    ordering = ['price']
    paginate_by = 6



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


class DiscountedProductsView(ListView):
    model = Product
    template_name = 'store/discounted_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True, has_discount=True).order_by('price')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_pk'



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('store:product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)


    if product.user != request.user and not request.user.is_superuser:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:product_detail', product_pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Update'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)


    if product.user != request.user and not request.user.is_superuser:
        return redirect('store:product_list')

    if request.method == 'POST':
        product.delete()
        return redirect('store:product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})