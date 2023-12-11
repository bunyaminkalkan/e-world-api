from rest_framework.generics import CreateAPIView
from .serializers import UserModel, UserCreateSerializer, UserRUDSerializer
from django.contrib.auth import login, authenticate


class UserCreateAPIView(CreateAPIView):
    '''
    View where users can create an account and log in immediately after creating it
    '''

    queryset = UserModel.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        from rest_framework import status
        from rest_framework.response import Response
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
    
    