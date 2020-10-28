from django.shortcuts import render
from .models import *
from working_scripts.rendering_scripts import get_pagination_info, get_tags


def index(request):
    # получаем теги и фильтр по ним
    tags, tags_filter = get_tags(request)

    recipes = Recipe.objects.all()
    if tags_filter:
        recipes = recipes.filter(tags_filter)

    # получаем пагинатор и номер страницы
    page, paginator = get_pagination_info(request, recipes)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }

    return render(request, 'index.html', context)
