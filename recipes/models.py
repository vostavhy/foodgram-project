from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()

# теги на старнице рецепта
BREAKFAST = 'breakfast'
LUNCH = 'lunch'
DINNER = 'dinner'

TAGS = ((BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'))


class RecipeQuerySet(models.QuerySet):

    def purchases(self, user):
        """список покупок одного пользователя"""
        return self.filter(purchases__user=user)

    def favorites(self, user):
        """список избранных рецептов одного пользователя"""
        return self.filter(favorites__user=user)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preparation_time = models.IntegerField(verbose_name='Время приготовления', help_text='в минутах')
    image = models.ImageField(upload_to='recipes/images/', verbose_name='Изображение', help_text='поле для рисунка')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    tags = MultiSelectField(choices=TAGS, default=BREAKFAST, verbose_name='Теги')

    # перегрузим Manager для данной модели
    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def ingredients(self):
        """получить список ингредиентов и их количества для определенного рецепта"""
        ingredients = (RecipeIngredient.objects.filter(recipe=self)
                       .select_related('ingredient')
                       .values_list('ingredient__title', 'amount', 'ingredient__dimension'))
        return ingredients

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Purchase(models.Model):
    """заказ для выгрузки списка ингридиентов в txt"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True, related_name='purchases',
                               verbose_name='Рецепт')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.recipe} в покупках у {self.user}'

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class Subscription(models.Model):
    """подписка на автора"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='Автор')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers', verbose_name='Пользователь')

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Ingredient(models.Model):
    """ингредиенты, из которых состоит рецепт"""
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    dimension = models.CharField(max_length=25, verbose_name='Единица измерения')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """промежуточная модель, объединяющая рецепты и ингредиенты"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='res_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_res',
                                   verbose_name='Ингредиент')
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Название рецепта: {self.recipe}. Ингридиент: {self.ingredient}'

    class Meta:
        ordering = ['-created_at', ]


class Favorite(models.Model):
    """избранные рецепты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites', verbose_name='Рецепт')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'для {self.user} избранный рецепт {self.recipe}'

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
