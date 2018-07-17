# ~*~ coding: utf-8 ~*~

from django import template
import urllib
from ..settings import rabbitmq_list, DATA_TMP_DIR
import json

register = template.Library()


@register.filter
def url_encode(value):
    return urllib.quote_plus(value)


@register.filter
def env_name(value):
    try:
        env_name = rabbitmq_list[value]['name']
    except:
        env_name = value
    return env_name


@register.simple_tag
def queue_consumers(cluster, vhost, queue):
    with open(DATA_TMP_DIR + '/queue_detail.json', 'r+') as f:
        json_str = json.load(f)
        try:
            if len(json_str[cluster][vhost][queue]) != 0:
                cluster = json_str[cluster][vhost][queue]
                print(type(cluster), cluster)
            else:
                cluster = ["no_cluster"]
        except KeyError:
            cluster = ["no_cached"]
    return cluster


@register.filter
def msg_translate(value):
    data_dic = {
        'no_cluster': '没有集群',
        'no_cached': '没有缓存',
        'channels': '通道',
        'consumers': '消费者',
        'queues': '消息队列',
        'connections': '连接',
        'vhost': '虚拟主机',
        'exchanges': '交换机',
        'messages': '消息总数',

    }
    try:
        return data_dic[value]
    except:
        return value


@register.filter
def byte_to_mb(value):
    return value / 1024 / 1024


@register.filter
def byte_to_gb(value):
    return value / 1024 / 1024 / 1024
