from django import template
register = template.Library()


@register.filter
def multiply(value, arg):
    print(value, ' ', arg)
    return round(value * arg, 2)
