from django.contrib import admin
from .models import Recipe, Purchase, Subscription, Ingredient, RecipeIngredient, \
    Favorite


class RecipeAdmin(admin.ModelAdmin):
    # поля, которые должны отобрадаться в админке
    list_display = ('pk', 'name', 'author', 'created_at', )
    # фильтрация по названию
    list_filter = ('name', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension',)
    # фильтрация по названию
    list_filter = ('title', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Purchase)
admin.site.register(Subscription)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
