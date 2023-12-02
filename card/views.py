from rest_framework.generics import ListCreateAPIView
from .serializers import Card, CardSerializer
from user.models import UserModel, User
from rest_framework.response import Response
from rest_framework import status

class CardListCreate(ListCreateAPIView):

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def post(self, request):
        #Add record
        user = UserModel.objects.get(username=request.data['username'])
        card = Card.objects.get(name=request.data['name'])
        print(user.balance, type(user.balance))
        if user.balance >= card.price:
            new_balance = user.balance - card.price
            user.balance = new_balance
            user.save()
            user.cards.add(card)
            return Response(status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
