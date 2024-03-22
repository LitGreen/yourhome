from django import template
import os

register = template.Library()

@register.filter
def has_image(image_field):
    if not image_field or not os.path.isfile(image_field.name):
        return False

    try:
        image_field.url
    except ValueError:
        return False
    else:
        return True