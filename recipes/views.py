from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from working_scripts.rendering_scripts import get_pagination_info, get_tags
from .forms import RecipeForm


def index(request, username=None):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    recipes = Recipe.objects.select_related('author')
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    title = 'Рецепты'
    template = 'index.html'
    author = None

    # если это страница профиля
    if '/user/' in request.path:
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
    recipes = Recipe.objects.favorites(user=request.user).select_related('author')
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    title = 'Избранное'
    template = 'favorite_index.html'
    items_on_page = 3

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes, per_page=items_on_page)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title,
    }

    return render(request, template, context)


@login_required
def subscription_index(request):
    authors = User.objects.filter(followers__user=request.user).prefetch_related('recipes')

    title = 'Мои подписки'
    template = 'subscription_index.html'
    items_on_page = 3

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, authors, per_page=items_on_page)

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
    ingredients_dict = dict()

    # с учетом того, что ингредиенты могут повторяться в разных рецептах,
    # составим сводный словарь списка игредиентов и их единиц измерения со всех рецептов в покупках
    for recipe in recipes:
        ingredients_list = recipe.ingredients
        for ingredient, amount in ingredients_list:

            # если ингредиент уже есть - добавляем его количество к уже имеющемуся значению
            if ingredient.title in ingredients_dict:
                ingredients_dict[ingredient.title][0] += amount

            # если нету - создаём
            else:
                ingredients_dict[ingredient.title] = [amount, ingredient.dimension]

    # добавим полученный словарь в файл и отдадим его в Response
    file = 'upload_files/purchase.txt'
    with open(file, 'w') as f:
        for ingredient_title, amount_dimension in ingredients_dict.items():
            print(f'{ingredient_title}: {amount_dimension[0]} {amount_dimension[1]}', file=f)

    response = FileResponse(open(file, 'rb'), as_attachment=True)
    return response


def recipe_index(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    template = 'recipe_index.html'

    context = {
        'recipe': recipe,
    }

    return render(request, template, context)


def recipe_create(request):
    template = 'recipe_create_form.html'
    form = RecipeForm()
    title = 'Создание рецепта'
    context = {
        'form': form,
        'title': title,

    }

    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            # списки названий игредиентов и их количества
            ingredient_titles = request.POST.getlist('nameIngredient')
            ingredient_amounts = request.POST.getlist('valueIngredient')
            if len(ingredient_titles) != len(ingredient_amounts):
                return render(request, template, context)

            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # после сохранения рецепта, добавим связующие модели между рецептом и игредиентами
            for i in range(len(ingredient_titles)):
                RecipeIngredient.objects.create(recipe=recipe,
                                                ingredient=Ingredient.objects.get(title=ingredient_titles[i]),
                                                amount=ingredient_amounts[i])
            return redirect('index')
        return render(request, template, context)
    return render(request, template, context)


def recipe_edit(request):
    return None


def recipe_delete(request):
    return None



