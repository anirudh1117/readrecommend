from django import template
from utils.common_function import get_categories_list

register = template.Library()

#@register.filter
#def getCategoryTag(categories):
#    return get_categories_list(categories)

def index(indexable, i):
    return indexable[i]

register.filter('index', index)

def remaining(indexable, items):
    if len(indexable) > len(items):
        return indexable[len(items)]
    return []

register.filter('remaining', remaining)