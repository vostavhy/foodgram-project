from django import template

register = template.Library()
from recipes.models import Purchase


@register.simple_tag
def set_tags(request, name):
    """устанавливаем GET параметры в зависимости от выбранных тегов"""
    # получим список тегов из url
    request_copy = request.GET.copy()
    tags_list = request_copy.getlist('tag')

    # если тег уже был выбран - удаляем его из GET параметров
    if name in tags_list:
        tags_list.remove(name)

    # если тег не был выбран, прописываем его в GET параметры
    else:
        tags_list.append(name)

    request_copy.setlist('tag', tags_list)
    return request_copy.urlencode()


@register.simple_tag
def set_page(request, page_number):
    """устанавливаем GET параметры в зависимости от выбранной страницы"""
    request_copy = request.GET.copy()
    request_copy['page'] = page_number
    return request_copy.urlencode()


@register.simple_tag
def set_purchase_number(request):
    """подсчет количества покупок"""
    number = Purchase.objects.filter(user=request.user).count()
    return number
