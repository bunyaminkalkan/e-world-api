from django.db import models
from django.contrib.auth.models import User
from card.models import Card
import os
from uuid import uuid4
from django_resized import ResizedImageField
from main.settings import MEDIA_ROOT


def path_and_rename(instance, filename):
    '''
    Function that reformats the profile photo uploaded by users and writes the new photo over it if they already have a profile photo
    '''
    upload_to = 'images/profiles/'
    ext = 'png'
    # get filename
    if instance.username:
        filename = '{}.{}'.format(instance.username, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    
    # if user has profile image overwrite old image
    path = str(MEDIA_ROOT)+ "/" + 'images/profiles/' + f"{filename}" # Path for users' profile photos

    if os.path.isfile(path):
        os.remove(path) # Remove old image
        return os.path.join(upload_to, filename)
    else:
        return os.path.join(upload_to, filename)

# inherite django.contrib.auth.models.user
class UserModel(User):
    '''
    Custom User Model for users 
    '''
    cards = models.ManyToManyField(Card, blank=True)
    balance = models.IntegerField(default=0)
    # ResizedImageField, resizes and crops the uploaded image
    profile_photo = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to=path_and_rename, null=True, blank=True, default="images/profiles/default.png")

    def __str__(self):
        return self.username
    
    def view_profile_photo(self):
        from django.utils.safestring import mark_safe
        if self.profile_photo:
            return mark_safe(f'<img src={self.profile_photo.url} style="max-height:150px; max-width:150px;"></img>')
        return mark_safe(f'<h2>No Profile Photo</h2>')
