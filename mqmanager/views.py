#!/usr/bin/python
# -*- coding:utf8 -*-
from django.shortcuts import render
from common import *
import datetime
from django.contrib.auth.decorators import login_required
from users.models import User
from rabbitmq.models import Auditlog
from settings import rabbitmq_list

@require_role(role='user')
def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    users_count = User.objects.filter(is_superuser=False).count()
    admins_count = User.objects.filter(is_superuser=True).count()
    cluster_count = len([k for k,v in rabbitmq_list.items()])
    today_operate = Auditlog.objects.all().count()
    return render(request, 'index.html', locals())