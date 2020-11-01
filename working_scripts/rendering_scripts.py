from django.core.paginator import Paginator
from django.db.models import Q
import operator
from functools import reduce


def get_pagination_info(request, posts, per_page=6):
    """
    request = HttpRequest object
    posts - posts needed for showing
    per_page - how many posts you want to show on one page
    return 'page' and 'paginator'
    """
    paginator = Paginator(posts, per_page)  # показывать по 6 записей на странице
    page_number = request.GET.get('page')  # переменная в url с номером запрошеной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return page, paginator


def get_tags(request):
    """фильтрация рецептов по тегам"""

    # получаем список переменных с названием тега
    tags = request.GET.getlist('tag')

    if tags:
        tags_filter = reduce(operator.or_, (Q(tags__contains=tag) for tag in tags))
        return tags, tags_filter

    return tags, None
