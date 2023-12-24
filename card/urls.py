from django.urls import path
from .views import CardListPurchaseAPIView, InventoryListAPIView, FactionListAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', CardListPurchaseAPIView.as_view()),
    path('factions/', FactionListAPIView.as_view()),
    path('inventory/<str:username>/', InventoryListAPIView.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)