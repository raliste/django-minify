import time

from django import template
from django.conf import settings

register = template.Library()

def _build_html(items, wrapping):
    if settings.DEBUG:
        wrapping = wrapping.replace('%s', '%s?t=' + str(time.time()))
        
    return '\n'.join((wrapping % (settings.STATIC_URL + item)) for item in items)

@register.simple_tag
def css(bundle):
    if settings.DEBUG:
        items = settings.MINIFY_BUNDLES['css'][bundle]
    else:
        items = (settings.STATIC_NAMES['css'][bundle],)
    return _build_html(items, '<link rel="stylesheet" type="text/css" href="%s" />')

@register.simple_tag
def js(bundle):
    if settings.DEBUG:
        items = settings.MINIFY_BUNDLES['js'][bundle]
    else:
        items = (settings.STATIC_NAMES['js'][bundle],)
    return _build_html(items, '<script type="text/javascript" src="%s"></script>')
    
