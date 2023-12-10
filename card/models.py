from django.db import models

class Card(models.Model):

    REGIONS = (
        (1, "-"),
        (2, "-"),
        (3, "-"),
        (4, "-"),
    )

    RARITYS = (
        (1, "Legendary"),
        (2, "Epic"),
        (3, "Rare"),
        (4, "Common"),
    )

    cardname = models.CharField(unique=True, max_length=64)
    detail = models.TextField(null=True, blank=True)
    faction = models.PositiveSmallIntegerField(choices=REGIONS, null=True, blank=True)
    rarity = models.PositiveSmallIntegerField(choices=RARITYS, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.cardname