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
    
    def view_flag(self):
        from django.utils.safestring import mark_safe
        if self.flag:
            return mark_safe(f'<img src={self.flag.url} style="height:200px; width:150px;"></img>')
        return mark_safe(f'<h2>No Flag</h2>')


class Card(models.Model):
    '''
    Card Model for cards of world
    '''
    
    cardname = models.CharField(unique=True, max_length=64)
    detail = models.TextField(null=True, blank=True)
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT)
    price = models.IntegerField(null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images/cards/", null=True, blank=True)

    def __str__(self):
        return self.cardname
    
    def view_image(self):
        from django.utils.safestring import mark_safe
        if self.image:
            return mark_safe(f'<img src={self.image.url} style="height:200px; width:150px;"></img>')
        return mark_safe(f'<h2>No Image</h2>')