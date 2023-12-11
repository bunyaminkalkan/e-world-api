from django.urls import path, include
from .views import UserCreateAPIView, UserRUDAPIView #,Logout

urlpatterns = [
    # path('auth/logout/', Logout.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('create/', UserCreateAPIView.as_view()),
    path('update/<str:username>', UserRUDAPIView.as_view()),
]
