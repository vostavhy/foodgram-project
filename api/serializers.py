from rest_framework import serializers

from recipes.models import Favorite, Ingredient, Purchase, Subscription


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = '__all__'
        model = Purchase


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.IntegerField

    class Meta:
        model = Favorite
        fields = ['recipe', 'user', 'id']
        read_only_fields = ['recipe']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.IntegerField

    class Meta:
        model = Subscription
        fields = ['author', 'user', 'id']
        read_only_fields = ['author']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient
