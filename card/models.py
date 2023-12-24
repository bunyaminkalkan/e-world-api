from django.db import models

class Faction(models.Model):
    '''
    Faction Model for card model
    '''

    faction_name = models.CharField(unique=True, max_length=64)
    history = models.TextField(null=True, blank=True)
    flag = models.ImageField(upload_to="images/factions/", null=True, blank=True)

    def __str__(self):
        return self.faction_name


class Card(models.Model):
    '''
    Card Model for cards of world
    '''
    
    cardname = models.CharField(unique=True, max_length=64)
    detail = models.TextField(null=True, blank=True)
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images/cards/", null=True, blank=True)

    def __str__(self):
        return self.cardname