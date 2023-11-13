from rest_framework.generics import CreateAPIView, GenericAPIView
from .serializers import UserModel, UserSerializer
from django.contrib.auth import login, authenticate, logout


class UserCreateApiView(CreateAPIView):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

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
        token = Token.objects.create(user=user)
        data['key'] = token.key
        # </--->
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        login(request, user)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class Logout(GenericAPIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
    