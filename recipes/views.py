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
    items_on_page = 6

    # если это страница профиля
    if '/user/' in request.path:
        author = get_object_or_404(User, username=username)
        recipes = recipes.filter(author=author)
        title = author.get_full_name()
        template = 'profile_index.html'

    # если это страница избранного
    if request.path == '/favorite/':
        recipes = recipes.filter(favorites__user=request.user)
        title = 'Избранное'
        items_on_page = 3
        template = 'favorite_index.html'

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes, per_page=items_on_page)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title,
        'author': author
    }

    return render(request, template, context)


def new_recipe(request):
    return None


def recipe_edit(request):
    return None


def recipe_delete(request):
    return None


def follow_index(request):
    return None


def favorite_index(request):
    return None


def purchase_index(request):
    return None


def recipe_index(request):
    return None
