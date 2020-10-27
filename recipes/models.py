from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()

# теги на старнице рецепта
TAGS = (('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'))


class RecipeQuerySet(models.QuerySet):
    # рецепты по тегу
    def recipes_tag(self, tag):
        return self.filter(tags__contains=tag)

    # список рецептов одного пользователя
    def recipes_author(self, user):
        return self.filter(author=user)

    # список рецептов нескольких авторов
    def recipes_authors(self, users):
        return self.filter(author__in=users)

    # список покупок одного пользователя
    def recipe_orders(self, user):
        return self.filter(orders__user=user)

    # список избранных рецептов одного пользователя
    def recipe_favorites(self, user):
        return self.filter(favorites__user=user)


class Test(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    tags = MultiSelectField(choices=TAGS, blank=True, null=True)

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return f'Name: {self.name} tags: {self.tags}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField(verbose_name='Описание')
    preparation_time = models.IntegerField()  # время приготовления в минутах
    image = models.ImageField(upload_to='recipes/images/')  # поле для рисунка
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    tags = MultiSelectField(choices=TAGS, blank=True, null=True)

    # перегрузим Manager для данной модели
    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def ingredients(self):
        return Ingredient.objects.filter(ingredient_res__recipe=self)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Order(models.Model):
    """заказ для выгрузки списка ингридиентов в txt"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True, related_name='orders')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class Follow(models.Model):
    """подписка на автора"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')  # на кого подписываются
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')  # кто подписывается

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Unit(models.Model):
    """единица измерения ингредиента"""
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'


class Ingredient(models.Model):
    """ингредиенты, из которых состоит рецепт"""
    name = models.CharField(max_length=100, db_index=True, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """промежуточная модель, объединяющая рецепты и ингредиенты"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_res')
    amount = models.IntegerField()
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Название рецепта: {self.recipe}. Ингридиент: {self.ingredient}'

    class Meta:
        ordering = ['-created_at', ]


class Favorite(models.Model):
    """избранные рецепты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')  # избранное для пользователя
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'для {self.user} избранный рецепт {self.recipe}'

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Избранное'
