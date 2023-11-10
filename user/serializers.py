from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        ]