from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from recipes.models import Purchase, Recipe, Favorite, Subscription, User, Ingredient
from .serializers import PurchaseSerializer, IngredientSerializer, FavoriteSerializer, SubscriptionSerializer
from .permissions import IsOwnerOrReadOnly


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
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка покупок."""
        instance = get_object_or_404(Purchase, recipe_id=int(kwargs['pk']), user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        """добавление рецепта в список избранного."""
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка избранного."""
        instance = get_object_or_404(Favorite, recipe_id=int(kwargs['pk']), user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        """добавление рецепта в список подписки."""
        author_id = int(self.request.data.get('id'))
        author = get_object_or_404(User, id=author_id)
        Subscription.objects.create(author=author, user=request.user)
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка подписки."""
        instance = get_object_or_404(Subscription, author_id=int(kwargs['pk']), user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class IngredientView(APIView):

    def get(self, request):
        query = request.GET.get('query').lower()
        ingredients = Ingredient.objects.filter(title__contains=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
