from django import template

register = template.Library()

@register.filter
def filename(value):
    return value.name.split('/')[-1]