from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [
            UniqueValidator(queryset=UserModel.objects.all())
        ],
    )

    password = serializers.CharField(
        write_only = True,  # GET methods can not return the password
        required = True,
        validators = [validate_password],
        style = {'input_type':'password',}
    )

    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type':'password',}
    )

    class Meta:
        model = UserModel
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = UserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            data = {
                "password": "Password fields does not match!!!"
            }
            raise serializers.ValidationError(data)
        return data
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
    
    
from dj_rest_auth.serializers import TokenSerializer

class UserTokenSerializer(TokenSerializer):

    user = UserCreateSerializer()

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')