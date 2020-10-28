from django import template
from recipes.models import Follow, Order, Favorite
register = template.Library()


@register.filter
def check_follow(author, user):
    """подписан ли текущий пользователь на автора"""
    return Follow.objects.filter(author_id=author.id, user_id=user.id).exists()


@register.filter
def check_order(recipe, user):
    """присутствует ли рецепт в спике покупок пользователя"""
    return Order.objects.filter(recipe_id=recipe.id, user_id=user.id).exists()


@register.filter
def check_favorite(recipe, user):
    """присутствует ли рецепт в спике покупок пользователя"""
    return Favorite.objects.filter(recipe_id=recipe.id, user_id=user.id).exists()
