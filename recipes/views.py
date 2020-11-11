from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from working_scripts.rendering_scripts import get_pagination_info, get_tags

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, User


def index(request):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    recipes = Recipe.objects.select_related('author')
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    title = 'Рецепты'
    template = 'index.html'
    author = None

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title,
        'author': author
    }

    return render(request, template, context)


def profile_index(request, username):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    recipes = Recipe.objects.select_related('author')
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    author = get_object_or_404(User, username=username)
    recipes = recipes.filter(author=author)
    title = author.get_full_name()
    template = 'profile_index.html'

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title,
        'author': author
    }

    return render(request, template, context)


@login_required
def favorite_index(request):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    # выгружаем рецепты в избранном у авторизованного пользователя
    recipes = (Recipe.objects.
               favorites(user=request.user).select_related('author'))
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    title = 'Избранное'
    template = 'favorite_index.html'
    items_on_page = 3

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request,
                                          recipes,
                                          per_page=items_on_page)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title,
    }

    return render(request, template, context)


@login_required
def subscription_index(request):
    authors = (User.objects.
               filter(followers__user=request.user).
               prefetch_related('recipes'))

    title = 'Мои подписки'
    template = 'subscription_index.html'
    items_on_page = 3

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request,
                                          authors,
                                          per_page=items_on_page)

    context = {
        'page': page,
        'paginator': paginator,
        'title': title,
    }

    return render(request, template, context)


@login_required
def purchase_index(request):
    recipes = Recipe.objects.purchases(user=request.user)

    title = 'Список покупок'
    template = 'purchase_index.html'

    context = {
        'recipes': recipes,
        'title': title
    }

    return render(request, template, context)


@login_required
def download_purchase_list(request):

    recipes = Recipe.objects.purchases(user=request.user)
    ingredients = dict()

    # с учетом того, что ингредиенты могут повторяться в разных рецептах,
    # составим сводный словарь списка игредиентов
    # и их единиц измерения со всех рецептов в покупках
    for recipe in recipes:
        for title, amount, dimension in recipe.ingredients:
            ingredients[title] = ingredients.get(title, [0, dimension])
            ingredients[title][0] += amount

    # добавим полученный словарь в файл и отдадим его в Response
    file_name = 'Purchase list.txt'
    txt = ''
    for ingredient_title, amount_dimension in ingredients.items():
        txt += (f'{ingredient_title}: '
                f'{amount_dimension[0]} {amount_dimension[1]} \n')

    response = HttpResponse(txt, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response


def recipe_index(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    template = 'recipe_index.html'

    context = {
        'recipe': recipe,
    }

    return render(request, template, context)


@login_required
def recipe_create(request):
    template = 'recipe_form.html'
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    title = 'Создание рецепта'
    button_name = 'Создать рецепт'
    context = {
        'form': form,
        'title': title,
        'button_name': button_name
    }

    if form.is_valid():
        # списки названий игредиентов и их количества
        ingredient_titles = request.POST.getlist('nameIngredient')
        ingredient_amounts = request.POST.getlist('valueIngredient')
        if len(ingredient_titles) != len(ingredient_amounts):
            return render(request, template, context)

        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        # добавим связующие модели между рецептом и игредиентами
        for title, amount in zip(ingredient_titles, ingredient_amounts):
            ingredient = get_object_or_404(Ingredient, title=title)
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)
        return redirect('index')
    return render(request, template, context)


@login_required
def recipe_edit(request, pk):
    # только автор может редактировать рецепт
    recipe = get_object_or_404(Recipe, author=request.user, id=pk)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)

    template = 'recipe_form.html'
    title = 'Редактирование рецепта'
    button_name = 'Сохранить'
    checked_tags = recipe.tags
    context = {
        'recipe': recipe,
        'form': form,
        'title': title,
        'button_name': button_name,
        'checked_tags': checked_tags,
    }

    if form.is_valid():
        # списки названий игредиентов и их количества
        ingredient_titles = request.POST.getlist('nameIngredient')
        ingredient_amounts = request.POST.getlist('valueIngredient')
        if len(ingredient_titles) != len(ingredient_amounts):
            return render(request, template, context)

        form.save()

        # чтобы не дублировались ингредиенты
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        # добавим связующие модели между рецептом и игредиентами заново
        for title, amount in zip(ingredient_titles, ingredient_amounts):
            ingredient = get_object_or_404(Ingredient, title=title)
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)
        return redirect('recipe_index', pk=recipe.id)
    return render(request, template, context)


@login_required
def recipe_delete(request, pk):
    # только автор может удалить рецепт
    recipe = get_object_or_404(Recipe, author=request.user, id=pk)
    recipe.delete()
    return redirect('index')
