from django.shortcuts import render
from .models import *
from working_scripts.rendering_scripts import get_pagination_info, get_tags


def index(request):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    recipes = Recipe.objects.select_related('author')
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes)

    title = 'Рецепты'
    if request.user.is_authenticated:
        title = request.user.first_name

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'title': title
    }

    return render(request, 'index.html', context)


def new_recipe(request):
    return None


def recipe_view(request):
    return None


def recipe_edit(request):
    return None


def recipe_delete(request):
    return None


def profile(request):
    return None


def profile_follow(request):
    return None


def profile_unfollow(request):
    return None


def follow_index(request):
    return None


def favorite_index(request):
    return None


def favorite_add(request):
    return None


def favorite_delete(request):
    return None


def order_index(request):
    return None


def order_add(request):
    return None


def order_delete(request):
    return None