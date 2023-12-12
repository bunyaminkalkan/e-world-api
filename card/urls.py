from django.urls import path
from .views import CardListPurchaseAPIView, InventoryListAPIView

urlpatterns = [
    path('', CardListPurchaseAPIView.as_view()),
    path('inventory/<str:username>/', InventoryListAPIView.as_view())
]
