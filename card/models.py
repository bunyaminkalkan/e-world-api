from django.db import models

class Card(models.Model):
    '''
    Card Model for cards of world
    '''
    
    REGIONS = (
        (1, "Ferhat Empire"),
        (2, "Hilito Empire"),
        (3, "Barış Empire"),
        (4, "Müno Empire"),
    )

    cardname = models.CharField(unique=True, max_length=64)
    detail = models.TextField(null=True, blank=True)
    faction = models.PositiveSmallIntegerField(choices=REGIONS, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images/cards/", null=True, blank=True)

    def __str__(self):
        return self.cardname