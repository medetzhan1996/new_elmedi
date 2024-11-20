from django import template
register = template.Library()


@register.simple_tag
def is_selected(val1, val2):
    if str(val1) == str(val2):
        return 'selected'
    return ''


@register.simple_tag
def is_checked(val):
    if val:
        return 'checked'
    return ''


@register.simple_tag
def get_val_by_percent(val, perc):
    if perc:
        return float(val)*float((perc/100))
    return val


@register.simple_tag
def is_leaf_node(data):
    if data:
        return True
    return


@register.simple_tag
def define(val=None):
    return val


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.simple_tag
def is_perfomed(val):
    if val:
        return 'checked'
    return ''