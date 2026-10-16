from django.db.models import Count
from .models import Category


def categories_processor(request):
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)

    return {
        'categories': categories
    }