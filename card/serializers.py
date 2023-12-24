from rest_framework import serializers
from .models import Card, Faction

class CardSerializer(serializers.ModelSerializer):
    '''
    Card Serializer for Card Views
    '''

    class Meta:
        model = Card
        exclude = []

class FactionSerializer(serializers.ModelSerializer):
    '''
    Faction Serializer for Faction List View
    '''
    
    class Meta:
        model = Faction
        exclude = []

