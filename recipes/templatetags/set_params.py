from django import template

register = template.Library()


@register.simple_tag
def set_tags(request, name):
    """устанавливаем GET параметры в зависимости от выбранных тегов"""
    # получим список тегов из url
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tag')

    # если тег уже был выбран - удаляем его из GET параметров
    if name in tags:
        tags.remove(name)

    # если тег не был выбран, прописываем его в GET параметры
    else:
        tags.append(name)

    request_copy.setlist('tag', tags)
    return request_copy.urlencode()


@register.simple_tag
def set_page(request, page_number):
    """устанавливаем GET параметры в зависимости от выбранной страницы"""
    request_copy = request.GET.copy()
    request_copy['page'] = page_number
    return request_copy.urlencode()
