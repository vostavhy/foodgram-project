from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                            Subscription, User)

from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """получение списка рецептов."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """добавление рецепта в список покупок."""
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка покупок."""
        instance = get_object_or_404(Purchase,
                                     recipe_id=int(kwargs.get('pk')),
                                     user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        """добавление рецепта в список избранного."""
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка избранного."""
        instance = get_object_or_404(Favorite,
                                     recipe_id=int(kwargs.get('pk')),
                                     user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """добавление рецепта в список покупок."""
        author_id = int(self.request.data.get('id'))
        author = get_object_or_404(User, id=author_id)
        serializer.save(user=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        """удаление подписки на автора."""
        instance = get_object_or_404(Subscription,
                                     author_id=(kwargs.get('pk')),
                                     user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def list(self, request, *args, **kwargs):
        """получим список ингредиентов."""
        query = request.GET.get('query').lower()
        queryset = self.queryset.filter(title__contains=query)
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)
