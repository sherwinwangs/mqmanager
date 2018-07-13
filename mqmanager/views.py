#!/usr/bin/python
# -*- coding:utf8 -*-
from django.shortcuts import render
from common import *

from django.contrib.auth.decorators import login_required


@require_role(role='user')
def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    return render(request, 'index.html', locals())
