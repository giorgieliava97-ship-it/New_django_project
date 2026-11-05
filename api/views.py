from rest_framework.decorators import api_view
from store.models import Product
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    products = Product.objects.values()
    return Response(products)
