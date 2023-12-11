from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import Card, CardSerializer
from user.models import UserModel
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthenticatedAndOwnData
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CardListCreateAPIView(ListCreateAPIView):
    '''
    Card list and for users to purchase cards view
    If method is GET all cards are listed
    If method is POST the logged user can purchase a card if his/her balance is sufficient.
    '''

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) # Permission class that anyone can view but only logged in users can make purchases

    def post(self, request):
        # Add record manytomany table for purchase
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
        

# user inventory view, lists cards the user has
class InventoryListAPIView(ListAPIView):
    '''
    Showing the cards users have purchased
    Users can only access their own inventory
    '''
    
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticatedAndOwnData,)
    # Accsess cards with username
    def get_queryset(self):
        user = UserModel.objects.get(username=self.kwargs['username'])
        queryset = user.cards.values()
        return queryset
        
