from rest_framework.generics import CreateAPIView, GenericAPIView
from .serializers import UserModel, UserRegisterSerializer, UserRUDSerializer, LoginSerializer, LogoutSerializer
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework import status


class UserRegisterAPIView(CreateAPIView):
    '''
    View where users can create an account and log in immediately after creating it
    '''

    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        from rest_framework.authtoken.models import Token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Defaults:
        serializer.validated_data['is_superuser'] = False
        serializer.validated_data['is_staff'] = False
        serializer.validated_data['is_active'] = True
        # Promotions
        promotion_chars = ('e', 'm', 'i', 'r', 'o', 'z', 't', 'u', 'k')
        username = serializer.validated_data['username'].lower()
        promotion_number = set()
        for char in username:
            char_lower = char.lower()
            if char_lower in promotion_chars and char not in promotion_number:
                promotion_number.add(char)
        # <--- User.save() & Token.create() --->
        user = serializer.save()
        user.balance += len(promotion_number) * 10
        user.save()
        data = serializer.data
        token = Token.objects.create(user=user) # Create token for user
        data['key'] = token.key
        # AutoLogin:
        user = authenticate(username=request.data['username'], password=request.data['password'])
        login(request, user)
        # Response
        headers = self.get_success_headers(serializer.data['username'])
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from card.permissions import IsAuthenticatedAndOwnData


class UserRUDAPIView(RetrieveUpdateDestroyAPIView):
    '''
    View where logged in users can retrieve, update and delete their own data
    '''

    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticatedAndOwnData,)
    serializer_class = UserRUDSerializer
    lookup_field = 'username'

    # Password change
    def put(self, request, *args, **kwargs):
        '''
        Function for the user to update their data
        The current password must be the same as the old password and the new password must be entered correctly twice.
        The new password must be a password that passes password validation.
        '''

        user = UserModel.objects.get(username=self.kwargs['username'])
        flag_new = False
        flag_new2 = False
        flag_cur = False
        
        if request.data['current_password'] != '': # if current password not blank
            flag_cur = True
            current_password = request.data['current_password']
        if request.data['new_password'] != '': # if new password not blank
            flag_new = True
            new_password = request.data['new_password']
        if request.data['new_password2'] != '': # if new password2 not blank
            flag_new2 = True
            new_password2 = request.data['new_password2']

        if (flag_cur):# Check whether the given password is the same as the password in the database
            if (not user.check_password(current_password)):
                data = {"message": "Current Password is not correct!!!"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
              
        if (flag_cur and flag_new and flag_new2): # if filled all password field
            if(new_password == new_password2): # Check if new_password1 and new_password2 are the same
                if(current_password != new_password): # Check if the new_password is the same as the old password
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True) # Validate new password
                    user.set_password(new_password) # Set new password
                    user.save() # Save user
                    return self.update(request, *args, **kwargs)
                    
                else:
                    data = {"message": "New Password does not same old password!!!"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {"message": "New Password fields does not match!!!"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        elif(flag_cur or flag_new or flag_new2): # If it only fills one or two fields. If it fills three, it goes inside the if block
            data = {"message": "Fill the all password fields not one!!!"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        elif(self.kwargs['username'] != request.data['username']):
            if (UserModel.objects.filter(username=request.data['username']).exists()):
                data = {"message": "A user with that username already exists."}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif ('admin' in request.data['username']):
                data = {"message": "Did you really think you could get this username?"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            return self.update(request, *args, **kwargs)
        else:
            return self.update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        user = UserModel.objects.get(username=self.kwargs['username'])
        if user.profile_photo.url != '/media/images/profiles/default.png':
            user.profile_photo.delete(save=True)
        user.auth_token.delete()
        return self.destroy(request, *args, **kwargs)


from rest_framework.authtoken.models import Token

# Logout with post method
class LogoutAPIView(GenericAPIView):
    '''
    View to delete the token given in the header with the post method
    '''
    model = UserModel.objects.all()
    serializer_class =  LogoutSerializer

    def post(self, request):
        request.user.auth_token.delete() # Delete token
        logout(request) # Logout
        data = {'message': 'Logged out succesfully!'}
        return Response(data, status=status.HTTP_202_ACCEPTED)

# Login with post method  
class LoginAPIView(GenericAPIView):
    '''
    The view where the user can log in by entering his username and password.
    Balance information is sent to be displayed after log in
    '''
    
    model = UserModel.objects.all()
    serializer_class =  LoginSerializer

    def post(self, request):
        if UserModel.objects.filter(username=request.data['username']).exists(): # Check the username is correct
            user = UserModel.objects.get(username=request.data['username']) # Get user
            if user.check_password(request.data['password']): # Check the password is correct
                token, created = Token.objects.get_or_create(user=user) # If the user has a token, get it, otherwise create it
                balance = user.balance # Get balance for display
                login(request, user) # Login
                profile_photo = "http://127.0.0.1:8000" + user.profile_photo.url
                data = {
                    'username': request.data['username'],
                    'balance': balance,
                    'profile_photo': profile_photo,
                    'key': token.key
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {'message': 'Username or Password is not correct'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {'message': 'Username or Password is not correct'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    