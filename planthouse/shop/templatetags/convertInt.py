from django import template

register = template.Library()

@register.filter(name='convertInt')

def times(number):
    return int(number)