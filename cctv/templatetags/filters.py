from django import template

register = template.Library()

# value|sub:arg means value - arg
@register.filter
def sub(value, arg):
    return value - arg
