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

        user = UserModel.objects.get(username=self.kwargs['username'])
        if request.data['current_password']: # if current password not blank
            current_password = request.data['current_password']
            if request.data['new_password']: # if current password not blank
                if user.check_password(current_password): # Check password
                    if request.data['new_password'] == request.data['new_password2']: # Check new password is same
                        user.set_password(request.data['new_password']) # Set new password
                        user.save() # Save user
                        # data = {"message": "Password Change Successfully"}
                        return self.update(request, *args, **kwargs)
                    else:
                        data = {"new_password": "New_Password fields does not match!!!"}
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {"current_password": "current_password field does not match!!!"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                    data = {"new_password": "new_password field does not blank!!!"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.update(request, *args, **kwargs)



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
    
    