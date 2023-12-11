from django.urls import path
from .views import CardListCreateAPIView, InventoryListAPIView

urlpatterns = [
    path('', CardListCreateAPIView.as_view()),
    path('inventory/<str:username>/', InventoryListAPIView.as_view())
]
