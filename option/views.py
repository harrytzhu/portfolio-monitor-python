from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from option.models import Option
from option.serializers import OptionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()