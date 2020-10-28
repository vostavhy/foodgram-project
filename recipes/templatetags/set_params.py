from django import template

register = template.Library()


@register.simple_tag
def set_tags(request, tags, name):
    """устанавливаем GET параметры в зависимости от выбранных тегов"""
    request_copy = request.GET.copy()

    # если тег уже был выбран - удаляем его из GET параметров
    if request.GET.get(name):
        request_copy.pop(name)

    # если тег не был выбран, прописываем его и ранее установленные теги в GET параметры
    else:
        for tag in tags:
            request_copy[tag] = 'tag'
        request_copy[name] = 'tag'

    return request_copy.urlencode()


@register.simple_tag
def set_page(request, page_number):
    """устанавливаем GET параметры в зависимости от выбранной страницы"""
    request_copy = request.GET.copy()
    request_copy['page'] = page_number
    return request_copy.urlencode()
