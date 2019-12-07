from django import template
register = template.Library()

@register.filter
def select(dict, key):
    '''Returns the given key from a dictionary.'''
    return dict[key]
