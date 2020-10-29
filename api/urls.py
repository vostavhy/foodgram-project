from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PurchaseView, FavoriteView, SubscriptionView, IngredientView

app_name = 'api'

urlpatterns = [
    # список покупок
    path('purchases/', PurchaseView.as_view()),
    path('add_purchase/', PurchaseView.as_view()),
    path('del_purchase/<int:pk>/', PurchaseView.as_view()),

    # избранное
    path('add_favorite/', FavoriteView.as_view()),
    path('del_favorite/<int:pk>/', FavoriteView.as_view()),

    # подписки
    path('add_subscription/', SubscriptionView.as_view()),
    path('del_subscription/<int:pk>/', SubscriptionView.as_view()),

    # запрос ингридиента
    path('ingredients/', IngredientView.as_view()),

]
