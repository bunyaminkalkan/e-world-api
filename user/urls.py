from django.urls import path, include
from .views import UserCreateApiView, UserRetrieveUpdateDestroyAPIView #,Logout

urlpatterns = [
    # path('auth/logout/', Logout.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('create/', UserCreateApiView.as_view()),
    path('update/<str:username>', UserRetrieveUpdateDestroyAPIView.as_view()),
]
