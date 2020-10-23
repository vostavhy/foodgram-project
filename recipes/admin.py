from django.contrib import admin
from .models import Recipe, Order, Subscription, Unit, Ingredient, RecipeIngredient, \
    Favorite, Tag, RecipeTag, User

admin.site.register(Recipe)

