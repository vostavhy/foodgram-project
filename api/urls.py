from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'purchases', PurchaseViewSet)
router.register(r'favorites', FavoriteViewSet)


urlpatterns = [
    path('', include(router.urls)),
]











