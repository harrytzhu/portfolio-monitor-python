from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from stock.models import Stock
from stock.serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()