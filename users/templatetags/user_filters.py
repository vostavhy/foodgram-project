from django import template

register = template.Library()


@register.filter
def addclass(field, new_class):
    return field.as_widget(attrs={'class': new_class})
