from django import template

register = template.Library()


@register.filter
def addclass(field, new_class):
    """добавляет class к input полю формы"""
    return field.as_widget(attrs={'class': new_class})


@register.filter
def separate(recipes):
    """вовращает три последних рецепта из предоставленного списка"""
    return recipes[:3]


@register.filter
def get_count(recipes_count):
    """возвращает количество рецептов - 3"""
    return int(recipes_count) - 3
