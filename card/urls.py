from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CardListCreate, InventoryList

urlpatterns = [
    path('', CardListCreate.as_view()),
    path('inventory/<int:pk>/', InventoryList.as_view())
]
