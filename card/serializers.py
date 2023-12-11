from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    '''
    Card Serializer for Card Views
    '''
    
    class Meta:
        model = Card
        exclude = [
            'faction',
            'image',
        ]
