from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# user create serializer with validations
class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    User Create Serializer For UserRegisterAPIView
    Email must be unique, password1 and password2 must be the same,
    '''

    email = serializers.EmailField(
        write_only = True,
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
        user.set_password(password) # Hashing the password
        user.save() # Save hashed password
        return user

    def validate(self, data):
        if data.get('password') != data.get('password2'): # Verifying that passwords are the same
            data = {
                "password": "Password fields does not match!!!"
            }
            raise serializers.ValidationError(data)
        return data
    
# user update serializer for user update view    
class UserRUDSerializer(serializers.ModelSerializer):
    '''
    User Retrieve Update Destroy Seriazlier For UserRUDAPIView
    '''

    username = serializers.CharField(required = False)

    # User can change password
    current_password = serializers.CharField(
        write_only = True, 
        required = False,
        style = {'input_type':'password',}
    )

    new_password = serializers.CharField(
        write_only = True, 
        required = False,
        validators = [validate_password],
        style = {'input_type':'password',}
    )

    new_password2 = serializers.CharField(
        write_only = True, 
        required = False,
        style = {'input_type':'password',}
    )

    class Meta:
        model = UserModel
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_photo",
            "current_password",
            "new_password",
            "new_password2",
        ]
    
    
class LoginSerializer(serializers.ModelSerializer):
    '''
    Serializer for user login, balance read only
    '''
    
    balance = serializers.IntegerField(
        read_only = True
    )

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'balance')


class LogoutSerializer(serializers.ModelSerializer):
    '''
    Serializer for user logout
    '''

    class Meta:
        model = UserModel
        fields = ()