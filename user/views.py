from rest_framework.viewsets import ModelViewSet 
from .serializers import UserModel, UserSerializer

class UserMVS(ModelViewSet):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
