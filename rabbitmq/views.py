#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from mqmanager.settings import rabbitmq_list, DATA_TMP_DIR
from .utils import batch_exec
from django.contrib.auth.decorators import login_required
from mqmanager.common import require_role, ServerError
from models import Auditlog
import json


@require_role(role='user')
def cluster_list(request):
    app, action = "MQ集群", "集群列表"
    mq_cluster = rabbitmq_list
    return render(request, 'rabbitmq/cluster_list.html', locals())


@require_role(role='user')
def vhost_list(request):
    app, action = "虚拟主机", "虚拟主机列表"
    vhost_obj = batch_exec()
    vhost_list = vhost_obj.list_vhosts()
    return render(request, 'rabbitmq/vhost_list.html', locals())


@require_role(role='admin')
def vhost_create(request):
    app, action = "虚拟主机", "创建虚拟主机"
    r_data = request.POST
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    if request.method == 'POST':
        vhost = r_data.get('vhost', '').strip()
        cluster = r_data.getlist('cluster', '')
        try:
            if '' in [vhost, cluster]:
                error = '带*内容不能为空'
                raise ServerError(error)
        except:
            pass
        else:
            obj = batch_exec(cluster)
            messages = obj.create_vhost(vhost)
            Auditlog.objects.create(user=request.user, type='创建', cluster=json.dumps(r_data.getlist('cluster', '')),
                                    target=app,
                                    url=request.get_full_path(),
                                    method=request.method, data=json.dumps({'vhost': vhost}))
    return render(request, 'rabbitmq/vhost_create.html', locals())


@require_role(role='admin')
def vhost_delete(request):
    app, action = "虚拟主机", "删除虚拟主机"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_vhost(r_data['vhost'])
    Auditlog.objects.create(user=request.user, type='删除', cluster=r_data['cluster'], target=app,
                            url=request.get_full_path(),
                            method=request.method, data={'vhost': r_data['vhost']})
    return HttpResponse(200)


@require_role(role='user')
def permission_list(request):
    app, action = "虚拟主机", "虚拟主机权限列表"
    r_data = request.GET
    obj = batch_exec(request.GET['cluster'])
    permission_list = obj.list_permission(r_data['vhost'])
    return render(request, 'rabbitmq/permission_list.html', locals())


@require_role(role='admin')
def permission_create(request):
    app, action = "虚拟主机权限", "创建虚拟主机权限"
    f_data = request.GET
    obj = batch_exec(f_data['cluster'])
    user_list = obj.list_users()
    if request.method == 'POST':
        r_data = request.POST
        data = {"vhost": r_data['vhost'], "username": r_data['user'], "configure": r_data['configure'],
                "write": r_data['write'], "read": r_data['read']}
        messages = obj.create_permission(vhost=r_data['vhost'], user=r_data['user'], data=data)
        Auditlog.objects.create(user=request.user, type='创建', cluster=f_data['cluster'], target=app,
                                url=request.get_full_path(),
                                method=request.method, data=data)
    return render(request, 'rabbitmq/permission_create.html', locals())


@require_role(role='admin')
def permission_delete(request):
    app, action = "虚拟主机权限", "删除虚拟主机权限"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    data = {"username": r_data['username'], "vhost": r_data['vhost']}
    obj.delete_permission(r_data['vhost'], username=r_data['username'], data=data)
    Auditlog.objects.create(user=request.user, type='删除', cluster=r_data['cluster'], target=app,
                            url=request.get_full_path(),
                            method=request.method, data=data)
    return HttpResponse(200)


@login_required
def user_list(request):
    app, action = "用户", "用户列表"
    return True


@require_role(role='user')
def exchange_list(request):
    app, action = "交换机", "交换机列表"
    exchange_obj = batch_exec()
    exchange_list = exchange_obj.list_exchanges()
    return render(request, 'rabbitmq/exchange_list.html', locals())


@require_role(role='admin')
def exchange_create(request):
    app, action = "交换机", "创建交换机"
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec()
    vhost_distinct = list(set([j['name'] for i in obj.list_vhosts() for k, v in i.items() for j in v]))
    if request.method == 'POST':
        mq_clusters_selectd = request.POST.getlist('cluster', '')
        f_data = request.POST
        try:
            if '' in [mq_clusters_selectd, f_data['name']]:
                error = '带*内容不能为空'
                raise ServerError(error)
        except:
            pass
        else:
            arguments_list_str = ["alternate-exchange"]
            arguments_dic_str = {k: str(v) for k, v in f_data.items() if k in arguments_list_str and v}
            data = {"vhost": f_data['vhost'], "name": f_data['name'].strip(), "type": f_data['type'],
                    "durable": f_data['durable'],
                    "auto_delete": f_data['auto_delete'], "internal": f_data['internal'],
                    "arguments": arguments_dic_str}
            obj = batch_exec(mq_clusters_selectd)
            messages = obj.create_exchange(vhost=data['vhost'], exchange=data['name'].strip(), data=data)
            Auditlog.objects.create(user=request.user, type='创建', cluster=mq_clusters_selectd, target=app,
                                    url=request.get_full_path(),
                                    method=request.method, data=data)
    return render(request, 'rabbitmq/exchange_create.html', locals())


@require_role(role='user')
def binding_list(request):
    app, action = "交换机绑定", "查看交换机绑定"
    res = request.GET
    obj = batch_exec(res['cluster'])
    binding_list = obj.list_bindings(res['vhost'], res['exchange'])
    return render(request, 'rabbitmq/binding_list.html', locals())


@require_role(role='admin')
def binding_create(request):
    app, action = "交换机绑定", "添加交换机绑定"
    f_data = request.GET
    obj = batch_exec(f_data['cluster'])
    queue_list = obj.list_queues(vhost=f_data['vhost'])[0][f_data['cluster']]
    if request.method == 'POST':
        p_data = request.POST
        try:
            if '' in [p_data['destination'], p_data['routing_key']]:
                error = '带*内容不能为空'
                raise ServerError(error)
        except:
            pass
        else:
            data = {"vhost": p_data['vhost'], "source": p_data['exchange'], "destination_type": p_data['type'],
                    "destination": p_data['destination'], "routing_key": p_data['routing_key'].strip(),
                    "arguments": {}}
            messages = obj.create_binding(vhost=p_data['vhost'], exchange=p_data['exchange'], type=p_data['type'],
                                          destination=p_data['destination'], data=data)
            Auditlog.objects.create(user=request.user, type='创建', cluster=f_data['cluster'], target=app,
                                    url=request.get_full_path(),
                                    method=request.method, data=data)
    return render(request, 'rabbitmq/binding_create.html', locals())


@require_role(role='admin')
def binding_delete(request):
    app, action = "交换机绑定", "删除交换机绑定"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    data = {"vhost": r_data['vhost'], "source": r_data['exchange'], "destination": r_data['destination'],
            "destination_type": r_data['type'], "properties_key": r_data['properties_key']}
    obj.delete_binding(r_data['vhost'], r_data['exchange'], r_data['type'], r_data['destination'],
                       r_data['properties_key'], data=data)
    Auditlog.objects.create(user=request.user, type='删除', cluster=r_data['cluster'], target=app,
                            url=request.get_full_path(),
                            method=request.method, data=data)
    return HttpResponse(200)


@require_role(role='admin')
def exchange_delete(request):
    app, action = "交换机", "删除交换机"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_exchange(r_data['vhost'], r_data['exchange'])
    Auditlog.objects.create(user=request.user, type='删除', cluster=r_data['cluster'], target=app,
                            url=request.get_full_path(),
                            method=request.method, data={'vhost': r_data['vhost'], 'exchange': r_data['exchange']})
    return HttpResponse(200)


@require_role(role='user')
def queue_list(request):
    app, action = "队列", "队列列表"
    cluster_dic = {k: v['name'] for k, v in rabbitmq_list.items()}
    cluster_dic['all'] = "全部集群"
    cluster = request.GET.getlist('cluster', '')
    if cluster == ['all']:
        cluster = [k for k, v in rabbitmq_list.items()]
    obj = batch_exec(cluster)
    queue_list = obj.list_queues()
    return render(request, 'rabbitmq/queue_list.html', locals())


@require_role(role='admin')
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
        cluster = f_data.getlist('cluster', '')
        try:
            if '' in [f_data['name'], cluster]:
                error = '带*内容不能为空'
                raise ServerError(error)
        except:
            pass
        else:
            data = {"vhost": f_data['vhost'], "name": f_data['name'].strip(), "durable": f_data['durable'],
                    "auto_delete": f_data['auto_delete'], "arguments": arguments_dic}
            obj = batch_exec(cluster)
            create_queue_messages = obj.create_queue(vhost=data['vhost'], queue=data['name'].strip(), data=data)
            if f_data['exchange'] and f_data['routing_key']:
                binding_data = {"vhost": f_data['vhost'], "source": f_data['exchange'], "destination_type": "q",
                                "destination": f_data['name'], "routing_key": f_data['routing_key'].strip(),
                                "arguments": {}}
                create_binding_messages = obj.create_binding(vhost=f_data['vhost'], exchange=f_data['exchange'],
                                                             type="q",
                                                             destination=f_data['name'].strip(),
                                                             data=binding_data)
                messages = create_queue_messages + create_binding_messages
                Auditlog.objects.create(user=request.user, type='创建', cluster=f_data.getlist('cluster', ''),
                                        target='交换机绑定',
                                        url=request.get_full_path(),
                                        method=request.method, data=binding_data)
            else:
                messages = create_queue_messages
                Auditlog.objects.create(user=request.user, type='创建', cluster=f_data.getlist('cluster', ''), target=app,
                                        url=request.get_full_path(),
                                        method=request.method, data=data)

    return render(request, 'rabbitmq/queue_create.html', locals())


@require_role(role='admin')
def queue_delete(request):
    app, action = "消息队列", "删除消息队列"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    obj.delete_queue(r_data['vhost'], r_data['queue'])
    Auditlog.objects.create(user=request.user, type='删除', cluster=r_data['cluster'], target=app,
                            url=request.get_full_path(),
                            method=request.method, data={'vhost': r_data['vhost'], 'queue': r_data['queue']})
    return HttpResponse(200)


@require_role(role='user')
def queue_detail(request):
    app, action = "消息队列", "消息队列详情"
    r_data = request.GET
    obj = batch_exec(r_data['cluster'])
    queue_info = obj.detail_queue(r_data['vhost'], r_data['queue'])
    consumer_ip_list = set([i['channel_details']['peer_host'] for i in queue_info['consumer_details']])
    consumer_cluster_list = []
    with open(DATA_TMP_DIR + '/cmdb.json', 'rb') as f:
        json_obj = json.load(f)
        for ip in consumer_ip_list:
            try:
                consumer_cluster_list += json_obj[ip]
            except Exception, e:
                consumer_cluster_list.append('%s在KMS没找到' % ip)
    queue_info['consumer_ip_list'] = consumer_ip_list
    queue_info['consumer_cluster_list'] = consumer_cluster_list
    return render(request, 'rabbitmq/queue_detail.html', locals())


@require_role(role='admin')
def definitions_sync(request):
    app, action = "MQ集群", "集群配置同步"
    destination_cluster = request.GET.get('destination', '')
    cluster_list = rabbitmq_list.keys()
    if request.method == 'POST':
        messages = []
        p_data = request.POST
        export_config = batch_exec(p_data['source'])
        source_configuration = export_config.definitions_export()
        import_config = batch_exec(p_data['destination'])
        message = import_config.definitions_import(data=source_configuration)
        message['detail'] += '[%s --->  %s]' % (p_data['source'], p_data['destination'])
        messages.append(message)
        Auditlog.objects.create(user=request.user, type='同步', cluster=p_data['destination'], target=app,
                                url=request.get_full_path(),
                                method=request.method,
                                data={'source': p_data['source'], 'destination': p_data['destination']})
    return render(request, 'rabbitmq/definitions_sync.html', locals())


@require_role(role='user')
def audit_log(request):
    app, action = "操作日志", "查看MQ操作日志"
    log_list = Auditlog.objects.all()
    return render(request, 'rabbitmq/audit_log.html', locals())


@require_role(role='admin')
def queue_cluster_sync(request):
    cluster, vhost, queue, ip_list = "", "", "", []
    data = {cluster: {vhost: {queue: [ip_list]}}}
    for cluster in rabbitmq_list.keys():
        vhost_list = [vhost['name'] for vhost in batch_exec(cluster).list_vhosts()[0][cluster]]
        for vhost in vhost_list:
            for queue in batch_exec(cluster).list_queues(vhost)[0][cluster]:
                vhost = queue['vhost']
                queue = queue['name']
                app_list = batch_exec(cluster).queue_kylincluster(vhost, queue)
                if not data.has_key(cluster):
                    data[cluster] = {}
                if not data[cluster].has_key(vhost):
                    data[cluster][vhost] = {}
                if not data[cluster][vhost].has_key(queue):
                    data[cluster][vhost][queue] = app_list
    with open(DATA_TMP_DIR + '/queue_detail.json', 'w') as f:
        f.write(json.dumps(data))
    Auditlog.objects.create(user=request.user, type='缓存', cluster='所有集群', target='队列消费集群',
                            url=request.get_full_path(),
                            method=request.method,
                            data={})
    return render(request, 'rabbitmq/queue_sync.html', locals())
