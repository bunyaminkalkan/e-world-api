from rest_framework.generics import CreateAPIView
from .serializers import UserModel, UserCreateSerializer, UserRUDSerializer
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework import status


class UserCreateAPIView(CreateAPIView):
    '''
    View where users can create an account and log in immediately after creating it
    '''

    queryset = UserModel.objects.all()
    serializer_class = UserCreateSerializer

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
from django.contrib.auth.password_validation import validate_password

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




# from rest_framework.response import Response
# from rest_framework import status

#-------------logout with get method
# class Logout(GenericAPIView):
#     def get(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         data = {
#         'message': 'Logged out succesfully!'
#         }
#         return Response(data, status=status.HTTP_202_ACCEPTED)
    
    