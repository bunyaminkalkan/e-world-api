from django.db import models
from django.contrib.auth.models import User
from card.models import Card
import os
from uuid import uuid4
from django_resized import ResizedImageField
import shutil
from main.settings import MEDIA_ROOT


def path_and_rename(instance, filename):
    upload_to = 'images/profiles/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.username:
        filename = '{}.{}'.format(instance.username, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    # if user has profile image overwrite old image --- need update didnt overwrite
    path = 'images/profiles/' + f"{filename}"
    new_path = str(MEDIA_ROOT)+ "/" + path

    if os.path.isfile(new_path):
        os.remove(new_path)
        return os.path.join(upload_to, filename)
    else:
        return os.path.join(upload_to, filename)

# create custom usermodel inherite django.contrib.auth.models.user
class UserModel(User):
    cards = models.ManyToManyField(Card, blank=True)
    balance = models.IntegerField(default=5000)
    profile_photo = ResizedImageField(size=[100, 100], crop=['middle', 'center'],upload_to=path_and_rename, null=True, blank=True, default="images/profiles/default")

    def __str__(self):
        return self.username
