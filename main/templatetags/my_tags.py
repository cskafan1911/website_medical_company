from django import template

register = template.Library()


@register.simple_tag()
@register.filter()
def my_media(val):
    if val:
        return f"/media/{val}"

    return ''
