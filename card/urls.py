from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CardMVS

router = DefaultRouter()
router.register('', CardMVS)

urlpatterns = router.urls