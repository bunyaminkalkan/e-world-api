from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserMVS

router = DefaultRouter()
router.register('', UserMVS)

urlpatterns = router.urls
