from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer, StockViewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'description')


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('products',)

    def get_serializer_class(self):
        if self.action == 'list':
            return StockViewSerializer
        return StockSerializer