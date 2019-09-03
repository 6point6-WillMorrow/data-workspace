from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def get_attr(model, field):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(model, str(field)):
        return getattr(model, field)


@register.filter
def add_class(field, class_attr):
    if 'class' in field.field.widget.attrs:
        field.field.widget.attrs['class'] = '{} {}'.format(
            field.field.widget.attrs['class'],
            class_attr
        )
    else:
        field.field.widget.attrs['class'] = class_attr
    return field


@register.filter
def add_field_error(field):
    return add_class(field, '{}--error'.format(
        field.field.widget.attrs.get('class')
    ))


@register.filter
def not_set_if_none(value):
    if value in ['', None]:
        return format_html('<span class="unknown">Not set</span>')
    return value
