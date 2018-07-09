# ~*~ coding: utf-8 ~*~

from django import template
import urllib
from ..settings import rabbitmq_list
from rabbitmq.models import *

register = template.Library()


@register.filter
def url_encode(value):
    return urllib.quote_plus(value)


@register.filter
def env_name(value):
    return rabbitmq_list[value]['name']


@register.filter
def queue_consumers(queue):
    app = QueueInfo.objects.filter(name__exact=queue)
    if app:
        # return view.acls.all().values_list('name')
        return [i[0] for i in app.values_list('consumers')]
            #list(app.values('consumers'))
    else:
        return '没有消费者'

@register.filter
def queue_consumers_comment(queue):
    app = QueueInfo.objects.filter(name__exact=queue)
    if app:
        return [i[0] for i in app.values_list('comment')]
    else:
        return ''