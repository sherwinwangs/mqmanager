#!/usr/bin/python
# -*- coding:utf8 -*-
from django.shortcuts import render
from common import require_role
from users.models import User
from rabbitmq.models import Auditlog
from rabbitmq.utils import batch_exec
from settings import rabbitmq_list


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '403.html')


def permission_denied(request):
    return render(request, '500.html')


@require_role(role='user')
def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    # from database
    users_count = User.objects.filter(role='User').count()
    operators_count = User.objects.filter(role='Operator').count()
    admins_count = User.objects.filter(role='Admin').count()
    cluster_count = len([k for k, v in rabbitmq_list.items()])
    today_operate = Auditlog.objects.all().count()

    # from rabbitmq api
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec()
    mq_vhost_count = {k: len(v) for vhost in obj.list_vhosts() for k, v in vhost.items()}
    mq_cluster_overview = obj.overview()
    mq_cluster_node = obj.nodes()
    for mq_cluster in mq_clusters_list:
        mq_cluster_overview[mq_cluster]['object_totals']['vhost'] = mq_vhost_count[mq_cluster]
        mq_cluster_overview[mq_cluster]['node_info'] = mq_cluster_node[mq_cluster]
    return render(request, 'index.html', locals())
