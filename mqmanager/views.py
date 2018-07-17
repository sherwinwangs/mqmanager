#!/usr/bin/python
# -*- coding:utf8 -*-
from django.shortcuts import render
from common import *
import datetime
from django.contrib.auth.decorators import login_required
from users.models import User
from rabbitmq.models import Auditlog
from settings import rabbitmq_list
from rabbitmq.utils import *
import json

@require_role(role='user')
def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    # from database
    users_count = User.objects.filter(role='User').count()
    operators_count = User.objects.filter(role='Operator').count()
    admins_count = User.objects.filter(role='Admin').count()
    cluster_count = len([k for k,v in rabbitmq_list.items()])
    today_operate = Auditlog.objects.all().count()

    # from rabbitmq api
    mq_clusters_list = {k: v['name'] for k, v in rabbitmq_list.items()}
    obj = batch_exec()
    mq_vhost_count = {k:len(v) for vhost in obj.list_vhosts() for k,v in vhost.items()}
    mq_cluster_overview=obj.overview()
    mq_cluster_node = obj.nodes()
    for mq_cluster in mq_clusters_list:
        mq_cluster_overview[mq_cluster]['object_totals']['vhost']=mq_vhost_count[mq_cluster]
        mq_cluster_overview[mq_cluster]['node_info']=mq_cluster_node[mq_cluster]
    return render(request, 'index.html', locals())