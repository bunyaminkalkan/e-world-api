from rest_framework.viewsets import ModelViewSet
from .serializers import Card, CardSerializer

class CardMVS(ModelViewSet):

    queryset = Card.objects.all()
    serializer_class = CardSerializer
