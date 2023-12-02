from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CardListCreate

urlpatterns = [
    path('', CardListCreate.as_view())
]

