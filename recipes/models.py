from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()

# теги на старнице рецепта
TAGS = (('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'))


class RecipeQuerySet(models.QuerySet):

    # список рецептов одного пользователя
    def profile(self, user):
        return self.filter(author=user)

    # список рецептов нескольких авторов
    def authors(self, users):
        return self.filter(author__in=users)

    # список покупок одного пользователя
    def purchases(self, user):
        return self.filter(purchases__user=user)

    # список избранных рецептов одного пользователя
    def favorites(self, user):
        return self.filter(favorites__user=user)


class Test(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    tags = MultiSelectField(choices=TAGS, blank=True, null=True)

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return f'Name: {self.name} tags: {self.tags}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preparation_time = models.IntegerField(verbose_name='Время приготовления')  # в минутах
    image = models.ImageField(upload_to='recipes/images/', verbose_name='Изображение')  # поле для рисунка
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    tags = MultiSelectField(choices=TAGS, blank=True, null=True, verbose_name='Теги')

    # перегрузим Manager для данной модели
    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.name

    # получить список ингредиентов
    @property
    def ingredients(self):
        return Ingredient.objects.filter(ingredient_res__recipe=self)

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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_res',
                                   verbose_name='Ингредиент')
    amount = models.IntegerField()
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
