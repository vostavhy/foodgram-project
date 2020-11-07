from rest_framework import serializers
from recipes.models import Purchase, Favorite, Subscription


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = '__all__'
        model = Purchase


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = '__all__'
        model = Favorite


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = '__all__'
        model = Subscription


class IngredientSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    dimension = serializers.CharField(max_length=25)
