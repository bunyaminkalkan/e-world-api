from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    '''
    Card Serializer for Card Views
    '''
    
    class Meta:
        model = Card
        exclude = []

    def to_representation(self, instance):
        response = super(CardSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url # Relative path
        return response
