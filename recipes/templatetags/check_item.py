from django import template
from recipes.models import Subscription, Purchase, Favorite
register = template.Library()


@register.filter
def check_subscription(author, user):
    """подписан ли текущий пользователь на автора"""
    return Subscription.objects.filter(author_id=author.id, user_id=user.id).exists()


@register.filter
def check_purchase(recipe, user):
    """присутствует ли рецепт в спике покупок пользователя"""
    return Purchase.objects.filter(recipe_id=recipe.id, user_id=user.id).exists()


@register.filter
def check_favorite(recipe, user):
    """присутствует ли рецепт в спике покупок пользователя"""
    return Favorite.objects.filter(recipe_id=recipe.id, user_id=user.id).exists()