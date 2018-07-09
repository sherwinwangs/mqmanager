#!/usr/bin/python
# -*- coding:utf8 -*-


from django.shortcuts import render


def dashboard(request):
    app, action = "仪表盘", "仪表盘"
    return render(request, 'index.html', locals())
