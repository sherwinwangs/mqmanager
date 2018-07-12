# ~*~ coding: utf-8 ~*~

from django import template
import urllib
from ..settings import rabbitmq_list
import json
from rabbitmq.models import *

register = template.Library()


@register.filter
def url_encode(value):
    return urllib.quote_plus(value)


@register.filter
def env_name(value):
    return rabbitmq_list[value]['name']


@register.filter
def queue_consumers(cluster,vhost,queue):
    with open('/tmp/queue_detail.json','r+') as f:
        json_str = json.load(f)
        return json_str[cluster][vhost][queue]