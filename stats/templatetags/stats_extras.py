from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    """返回两个数的差值"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
