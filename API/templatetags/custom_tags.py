from django import template

register = template.Library()

@register.simple_tag
def get_id(document):
    return document['_id']