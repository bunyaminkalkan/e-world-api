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
        # <--- User.save() & Token.create() --->
        user = serializer.save()
        data = serializer.data
        token = Token.objects.create(user=user) # Create token for user
        data['key'] = token.key
        # AutoLogin:
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
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
    def patch(self, request, *args, **kwargs):
        '''
        Function for the user to update their data
        The current password must be the same as the old password and the new password must be entered correctly twice.
        The new password must be a password that passes password validation.
        '''

        user = UserModel.objects.get(username=self.kwargs['username'])
        flag_new = False
        flag_new2 = False
        flag_cur = False
        flag_che = False

        for data in request.data:
            if data == 'current_password': # if current password not blank
                flag_cur = True
                current_password = request.data['current_password']
            if data == 'new_password': # if new password not blank
                flag_new = True
                new_password = request.data['new_password']
            if data == 'new_password2': # if new password2 not blank
                flag_new2 = True
                new_password2 = request.data['new_password2']

        if (flag_cur and user.check_password(current_password)): # Check whether the given password is the same as the password in the database
            flag_che = True

        if (flag_cur and flag_new and flag_new2): # if filled all password field
            if(flag_che): # if password is correct
                if(new_password == new_password2): # Check if new_password1 and new_password2 are the same
                    if(current_password != new_password): # Check if the new_password is the same as the old password
                        serializer = self.get_serializer(data=request.data)
                        serializer.is_valid(raise_exception=True) # Validate new password
                        user.set_password(new_password) # Set new password
                        user.save() # Save user
                        return self.partial_update(request, *args, **kwargs)
                        
                    else:
                        data = {"current_password": "New_password does not same old password!!!"}
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {"new_password": "New_password fields does not match!!!"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {"current_password": "Current_password is not correct!!!"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        elif(flag_cur or flag_new or flag_new2): # If it only fills one or two fields. If it fills three, it goes inside the if block
            data = {"passwords": "Fill the all password fields not one!!!"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            return self.partial_update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        user = UserModel.objects.get(username=self.kwargs['username'])
        user.profile_photo.delete(save=True)
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
        data = {
        'message': 'Logged out succesfully!'
        }
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
                image = "http://127.0.0.1:8000" + user.profile_photo.url
                data = {
                    'username': request.data['username'],
                    'balance': balance,
                    'key': token.key,
                    'image': image
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {'wrong': 'username or password is not correct'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {'wrong': 'username or password is not correct'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    