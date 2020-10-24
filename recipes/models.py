from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.TextField(max_length=100, db_index=True, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    preparation_time = models.IntegerField()  # время приготовления в минутах
    image = models.ImageField(upload_to='recipes/images/')  # поле для рисунка
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)


class Order(models.Model):
    """заказ для выгрузки списка ингридиентов в txt"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)


class Subscription(models.Model):
    """подписка на автора"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes')  # на кого подписываются
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')  # кто подписывается


class Unit(models.Model):
    """единица измерения ингредиента"""
    name = models.TextField(max_length=100, blank=True, null=True)


class Ingredient(models.Model):
    """ингредиенты, из которых состоит рецепт"""
    name = models.TextField(max_length=100, db_index=True, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='ingredients')


class RecipeIngredient(models.Model):
    """промежуточная модель, объединяющая рецепты и ингредиенты"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)


class Favorite(models.Model):
    """избранные рецепты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')  # избранное для пользователя
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)


class Tag(models.Model):
    """завтрак, обед, ужин"""
    name = models.TextField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)


class RecipeTag(models.Model):
    """промежуточная модель, объединяющая рецепт и тег"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE)
