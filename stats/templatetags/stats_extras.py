from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def subtract(value, arg):
    """
    返回两个数字的差值
    用法: {{ value|subtract:arg }}
    """
    try:
        return value - arg
    except (ValueError, TypeError):
        return value


@register.filter
def percentage(value, total):
    """
    计算百分比
    用法: {{ value|percentage:total }}
    """
    try:
        if total == 0:
            return 0
        return round((Decimal(str(value)) / Decimal(str(total))) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def abs_value(value):
    """
    返回绝对值
    用法: {{ value|abs_value }}
    """
    try:
        return abs(value)
    except (ValueError, TypeError):
        return value
