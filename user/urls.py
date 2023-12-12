from django.urls import path
from .views import UserRegisterAPIView, UserRUDAPIView, LogoutAPIView, LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('update/<str:username>', UserRUDAPIView.as_view()),
]
