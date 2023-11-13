from django.urls import path, include
from .views import UserCreateApiView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('create/', UserCreateApiView.as_view()),
]
