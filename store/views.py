from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Category
from .forms import ProductForm
from django.db.models import Q, Count, Min, Max


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
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        category_id = self.request.GET.get('category')
        if category_id and category_id != '':
            queryset = queryset.filter(category_id=category_id)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by(
                '-created_at'
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__is_available=True))
        )
        context['categories'] = categories
        current_category_id = self.request.GET.get('category')
        context['selected_category_name'] = "All Products"
        if current_category_id:
            selected_cat = categories.filter(id=current_category_id).first()
            if selected_cat:
                context['selected_category_name'] = selected_cat.name

        price_stats = Product.objects.filter(is_available=True).aggregate(min=Min('price'), max=Max('price'))
        context['min_product_price'] = price_stats['min'] or 0
        context['max_product_price'] = price_stats['max'] or 5000
        context['current_search'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', '')
        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'store/category_products.html'
    context_object_name = 'products'
    paginate_by = 3

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
    paginate_by = 3

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