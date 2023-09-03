from django import template
from common_function import get_categories_list

register = template.Library()

@register.filter
def getCategoryTag(categories):
    return get_categories_list(categories)