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

    name = models.CharField(unique=True, max_length=64)
    detail = models.TextField()
    faction = models.PositiveSmallIntegerField(choices=REGIONS)
    rarity = models.PositiveSmallIntegerField(choices=RARITYS)
    price = models.IntegerField()
    power = models.IntegerField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name