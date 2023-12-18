from django.urls import path
from .views import UserRegisterAPIView, UserRUDAPIView, LogoutAPIView, LoginAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('update/<str:username>', UserRUDAPIView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)