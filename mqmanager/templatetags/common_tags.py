# ~*~ coding: utf-8 ~*~

from django import template
import urllib
from ..settings import rabbitmq_list

register = template.Library()


@register.filter
def url_encode(value):
    return urllib.quote_plus(value)


@register.filter
def env_name(value):
    return rabbitmq_list[value]['name']
