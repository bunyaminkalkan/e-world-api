from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import Card, CardSerializer
from user.models import UserModel
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthenticatedAndOwnData
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .pagination import CustomPageNumberPagination

class CardListPurchaseAPIView(ListCreateAPIView):
    '''
    Card list and for users to purchase cards view
    If method is GET all cards are listed and to be used in the frontend, if the user is logged in and has cards, show the price of the cards the user has as 0.
    If method is POST the logged user can purchase a card if his/her balance is sufficient.
    '''

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) # Permission class that anyone can view but only logged in users can make purchases
    pagination_class = CustomPageNumberPagination
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if request.user.is_authenticated: # if user is logged in
                user = UserModel.objects.get(id=request.user.id) # get user
                for i in range(len(user.cards.values_list())): # number of cards the user has
                    card_price = user.cards.values_list()[i][4] # get price for the cards the user has
                    for j in range(len(serializer.data)): # browse all cards
                        if card_price == serializer.data[j]['price']: # find cards owned by user
                            serializer.data[j]['price'] = 0 # set card price equal to 0
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Add record manytomany table for purchase
        user = UserModel.objects.get(username=request.data['username'])
        card = Card.objects.get(cardname=request.data['cardname'])
        if user.balance >= card.price:
            new_balance = user.balance - card.price
            new_price = card.price * 1.22
            user.balance = new_balance
            card.price = int(new_price)
            user.save()
            card.save()
            user.cards.add(card)
            data = {'balance': new_balance, 'purchase': 'Successfully'}
            return Response(data, status=status.HTTP_201_CREATED)
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
    pagination_class = CustomPageNumberPagination
    # Accsess cards with username
    def get_queryset(self):
        user = UserModel.objects.get(username=self.kwargs['username'])
        queryset = user.cards.values()
        return queryset
        