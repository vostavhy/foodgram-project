from rest_framework import serializers


class PurchaseSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    recipe = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField()


class IngredientSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    dimension = serializers.CharField(max_length=25)
