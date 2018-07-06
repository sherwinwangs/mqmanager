#!/usr/bin/python
# -*- coding:utf8 -*-

from django.views.generic import ListView
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, redirect, get_object_or_404
from django.core.paginator import Paginator
from settings import rabbitmq_list
from .utils import *
from django.http import HttpResponseRedirect


def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    return render(request, 'index.html', locals())


def cluster_list(request):
    app, action = "MQ集群", "集群列表"
    mq_cluster = rabbitmq_list
    return render(request, 'rabbitmq/cluster_list.html', locals())


def vhost_list(request):
    app, action = "虚拟主机", "虚拟主机列表"
    vhost_obj = batch_exec()
    vhost_list = vhost_obj.list_vhosts()
    return render(request, 'rabbitmq/vhost_list.html', locals())


def vhost_create(request):
    app, action = "虚拟主机", "创建虚拟主机"
    r_data = request.POST
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec(r_data.getlist('cluster', ''))
    messages = obj.create_vhost(r_data.get('vhost', ''))
    return render(request, 'rabbitmq/vhost_create.html', locals())


def vhost_delete(request):
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_vhost(r_data['vhost'])
    return HttpResponseRedirect('/vhost/list')


def permission_list(request):
    app, action = "虚拟主机", "虚拟主机权限列表"
    r_data = request.GET
    print(r_data)
    obj = batch_exec(request.GET['cluster'])
    permission_list = obj.list_permission(r_data['vhost'])
    return render(request, 'rabbitmq/permission_list.html', locals())


def permission_create(request):
    app, action = "虚拟主机", "虚拟主机权限添加"
    f_data = request.GET
    obj = batch_exec(request.GET['cluster'])
    user_list = obj.list_users()
    if request.method == 'POST':
        r_data = request.POST
        data = {"vhost": r_data['vhost'], "username": r_data['user'], "configure": r_data['configure'],
                "write": r_data['write'], "read": r_data['read']}
        messages = obj.create_permission(vhost=r_data['vhost'], user=r_data['user'], data=data)
    return render(request, 'rabbitmq/permission_create.html', locals())


# {"vhost":"qianbaoxiaodai","username":"base_csdnpay","configure":".*","write":".*","read":".*"}

def user_list(request):
    app, action = "用户", "用户列表"
    return True


def exchange_list(request):
    app, action = "交换机", "交换机列表"
    exchange_obj = batch_exec()
    exchange_list = exchange_obj.list_exchanges()
    return render(request, 'rabbitmq/exchange_list.html', locals())


def exchange_create(request):
    app, action = "交换机", "创建交换机"
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec()
    vhost_distinct = list(set([j['name'] for i in obj.list_vhosts() for k, v in i.items() for j in v]))
    if request.method == 'POST':
        mq_clusters_selectd = request.POST.getlist('cluster', '')
        f_data = request.POST
        arguments_list_str = ["alternate-exchange"]
        arguments_dic_str = {k: str(v) for k, v in f_data.items() if k in arguments_list_str and v}
        data = {"vhost": f_data['vhost'], "name": f_data['name'], "type": f_data['type'], "durable": f_data['durable'],
                "auto_delete": f_data['auto_delete'], "internal": f_data['internal'], "arguments": arguments_dic_str}
        obj = batch_exec(mq_clusters_selectd)
        messages = obj.create_exchange(vhost=data['vhost'], exchange=data['name'], data=data)
    return render(request, 'rabbitmq/exchange_create.html', locals())


def binding_list(request):
    app, action = "交换机", "交换机绑定"
    res = request.GET
    obj = batch_exec(res['cluster'])
    binding_list = obj.list_bindings(res['vhost'], res['exchange'])
    return render(request, 'rabbitmq/binding_list.html', locals())


def binding_create(request):
    app, action = "交换机", "添加绑定"
    f_data = request.GET
    obj = batch_exec(f_data['cluster'])
    queue_list = obj.list_queues(vhost=f_data['vhost'])[0][f_data['cluster']]
    if request.method == 'POST':
        print(request.POST)
        p_data = request.POST
        data = {"vhost": p_data['vhost'], "source": p_data['exchange'], "destination_type": p_data['type'],
                "destination": p_data['destination'], "routing_key": p_data['routing_key'],
                "arguments": {}}
        messages = obj.create_binding(vhost=p_data['vhost'], exchange=p_data['exchange'], type=p_data['type'],
                                      destination=p_data['destination'], data=data)
    return render(request, 'rabbitmq/binding_create.html', locals())


'''
    def create_binding(self, vhost, exchange, type, destination, data={}):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_binding(vhost, exchange, type, destination, data=data)
            res['detail'] = k + ':' + res['detail']
            messages.append(res)
        return messages
'''


def binding_delete(request):
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    data = {"vhost": r_data['vhost'], "source": r_data['exchange'], "destination": r_data['destination'],
            "destination_type": r_data['type'], "properties_key": r_data['properties_key']}
    obj.delete_binding(r_data['vhost'], r_data['exchange'], r_data['type'], r_data['destination'],
                       r_data['properties_key'], data=data)
    return HttpResponseRedirect('/exchanges/bindings/list?cluster=%s&vhost=%s&exchange=%s' % (
        r_data['cluster'], r_data['vhost'], r_data['exchange']))


def exchange_delete(request):
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_exchange(r_data['vhost'], r_data['exchange'])
    return HttpResponseRedirect('/exchange/list')


def queue_list(request):
    app, action = "队列", "队列列表"
    obj = batch_exec()
    queue_list = obj.list_queues()
    return render(request, 'rabbitmq/queue_list.html', locals())


def queue_create(request):
    app, action = "消息队列", "创建消息队列"
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec()
    vhost_distinct = list(set([j['name'] for i in obj.list_vhosts() for k, v in i.items() for j in v]))
    exchange_distinct = set([(j['name'], j['vhost']) for i in obj.list_exchanges() for k, v in i.items() for j in v])
    exchange_distinct_list = [{"name": i[0], "vhost": i[1]} for i in exchange_distinct]

    if request.method == 'POST':
        f_data = request.POST
        arguments_list_str = ["x-dead-letter-exchange", "x-dead-letter-routing-key"]
        arguments_list_int = ["x-message-ttl", "x-expires", "x-max-length"]
        arguments_dic_int = {k: int(v) for k, v in f_data.items() if k in arguments_list_int and v}
        arguments_dic_str = {k: str(v) for k, v in f_data.items() if k in arguments_list_str and v}
        arguments_dic = dict(arguments_dic_int, **arguments_dic_str)
        data = {"vhost": f_data['vhost'], "name": f_data['name'], "durable": f_data['durable'],
                "auto_delete": f_data['auto_delete'], "arguments": arguments_dic}
        obj = batch_exec(f_data.getlist('cluster', ''))
        create_queue_messages = obj.create_queue(vhost=data['vhost'], queue=data['name'], data=data)
        if f_data['exchange'] and f_data['routing_key']:
            binding_data = {"vhost": f_data['vhost'], "source": f_data['exchange'], "destination_type": "q",
                            "destination": f_data['name'], "routing_key": f_data['routing_key'],
                            "arguments": {}}
            create_binding_messages = obj.create_binding(vhost=f_data['vhost'], exchange=f_data['exchange'], type="q",
                                                         destination=f_data['name'],
                                                         data=binding_data)
            messages = create_queue_messages + create_binding_messages
        else:
            messages = create_queue_messages
    return render(request, 'rabbitmq/queue_create.html', locals())


def queue_delete(request):
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_queue(r_data['vhost'], r_data['queue'])
    return HttpResponseRedirect('/queue/list')


def test_url(request, *args, **kwargs):
    return render(request, '/test/test.html', locals())
