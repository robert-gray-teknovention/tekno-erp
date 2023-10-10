from django import template


register = template.Library()


def hello(value):
    return value


register.filter('hello', hello)
