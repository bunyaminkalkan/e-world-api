from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        exclude = [
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
            "cards",
            "is_staff",
            "is_active",
            "is_superuser",
        ]

    def validate(self, attrs):
        if attrs.get('password', False):
            from django.contrib.auth.password_validation import validate_password #doğrulama
            from django.contrib.auth.hashers import make_password #hashleme
            password = attrs['password'] #şifreyi al
            validate_password(password) #doğrulamadan geçir
            attrs.update(
                {
                    'password': make_password(password) # password şifrele ve güncelle
                }
            )
        return super().validate(attrs) #Orjinal metodu çalıştır