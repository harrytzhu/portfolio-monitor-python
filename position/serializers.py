from rest_framework import serializers

from .models import Position, PositionPrice


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        depth = 2

class PositionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionPrice
        fields = '__all__'
        depth = 2