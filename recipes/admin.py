from django.contrib import admin
from .models import Recipe, Order, Follow, Unit, Ingredient, RecipeIngredient, \
    Favorite


class RecipeAdmin(admin.ModelAdmin):
    # поля, которые должны отобрадаться в админке
    list_display = ('pk', 'name', 'author', 'created_at', )
    # фильтрация по названию
    list_filter = ('name', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit',)
    # фильтрация по названию
    list_filter = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Order)
admin.site.register(Follow)
admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)