from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from working_scripts.rendering_scripts import get_pagination_info, get_tags


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


def new_recipe(request):
    return None


def recipe_edit(request):
    return None


def recipe_delete(request):
    return None


def recipe_index(request):
    return None
