from django.http import JsonResponse, HttpResponse
from django.core import serializers
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from position import PricePublisher, QueueEngine
from position.serializers import PositionSerializer, PositionPriceSerializer
from position.models import Position, PositionPrice, Statistic


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


@api_view(["GET"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def statistic(request):
    if request.method == "GET":
        positions = PositionSerializer(instance=Position.objects.all(), many=True)
        price_dict: dict = QueueEngine.get()
        summary = 0.0
        position_price = PositionPrice()
        statistic = Statistic()
        statistic.prices = []
        for position in positions.data:
            symbol = position["symbol"]
            price = price_dict[position["symbol"]]
            position_price.symbol = symbol
            position_price.price = price
            position_price.size = position["size"]
            position_price.summary = float(price) * float(position["size"])
            statistic.prices.append(position_price)
            summary += position_price.summary
        statistic.summary = summary
        return HttpResponse(statistic.toJSON(), content_type='application/json',status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def start_publishing(request):
    if request.method == "POST":
        PricePublisher.start_publishing()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def stop_publishing(request):
    if request.method == "POST":
        PricePublisher.stop_publishing()
    return Response(status=status.HTTP_400_BAD_REQUEST)
