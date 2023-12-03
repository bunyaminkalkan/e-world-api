from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import Card, CardSerializer
from user.models import UserModel
from rest_framework.response import Response
from rest_framework import status

class CardListCreate(ListCreateAPIView):

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def post(self, request):
        #Add record for purchase
        user = UserModel.objects.get(username=request.data['username'])
        card = Card.objects.get(name=request.data['name'])
        if user.balance >= card.price:
            new_balance = user.balance - card.price
            user.balance = new_balance
            user.save()
            user.cards.add(card)
            return Response(status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class InventoryList(ListAPIView):
    serializer_class = CardSerializer
    #-------Accses cards with username
    def get_queryset(self):
        user = UserModel.objects.get(username=self.kwargs['username'])
        queryset = user.cards.values()
        return queryset
        
