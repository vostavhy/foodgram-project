from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import FavoriteView, SubscriptionView, IngredientView

from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet

router = DefaultRouter()
router.register(r'purchases', PurchaseViewSet)
urlpatterns = router.urls
