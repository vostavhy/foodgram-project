from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from recipes.models import Purchase, Recipe, Favorite, Subscription, User, Ingredient
from .serializers import PurchaseSerializer, IngredientSerializer
from .permissions import IsOwnerOrReadOnly


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """получение списка рецептов."""
        return Purchase.objects.filter(recipe__author=self.request.user)

    def perform_create(self, serializer):
        """добавление рецепта в список покупок."""
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        serializer.save(user=user, recipe=recipe)
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка покупок."""
        instance = get_object_or_404(Purchase, recipe_id=int(kwargs['pk']), user=request.user)
        self.perform_destroy(instance)
        return Response({"success": True})


class FavoriteView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    # добавление рецепта в список избранного
    def post(self, request):
        recipe_id = int(request.data.get('id'))
        recipe = Recipe.objects.get(id=recipe_id)
        Favorite.objects.create(recipe=recipe, user=request.user)
        return Response({"success": True})

    # удаление рецепта из списка избранного
    def delete(self, request, pk):
        favorite = get_object_or_404(Favorite.objects.all(), recipe_id=pk, user=request.user)
        favorite.delete()
        return Response({"success": True})


class SubscriptionView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    # подписаться на автора
    def post(self, request):
        author_id = int(request.data.get('id'))
        author = User.objects.get(id=author_id)
        Subscription.objects.create(author=author, user=request.user)
        return Response({"success": True})

    # удаление подписки
    def delete(self, request, pk):
        subscription = get_object_or_404(Subscription.objects.all(), author_id=pk, user=request.user)
        subscription.delete()
        return Response({"success": True})


class IngredientView(APIView):

    def get(self, request):
        query = request.GET.get('query').lower()
        ingredients = Ingredient.objects.filter(title__contains=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
