from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, PurchaseViewSet,
                    SubscriptionViewSet)

router = DefaultRouter()
router.register(r'purchases', PurchaseViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
