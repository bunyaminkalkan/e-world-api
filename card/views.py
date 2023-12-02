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
        user = UserModel.objects.filter(username=request.data['username']).values()
        card = Card.objects.filter(name=request.data['name']).values()
        if user.values_list('balance')[0][0] >= card.values_list('price')[0][0]:
            new_balance = user.values_list('balance')[0][0] - card.values_list('price')[0][0]
            user.update(balance=new_balance)
            user.cards.add(card)
            return Response(status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
