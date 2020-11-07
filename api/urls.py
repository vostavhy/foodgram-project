from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet, FavoriteViewSet, SubscriptionViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r'purchases', PurchaseViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]










