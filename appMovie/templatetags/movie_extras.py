from django import template

register = template.Library()


@register.filter
def data(value):
    return value.all()


@register.filter
def url(value):
    if '=' in value:
        value = value.split('=')
        return value[1]
    else:
        return value
