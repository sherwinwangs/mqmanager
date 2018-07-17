# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from mqmanager.common import require_role, ServerError
# Create your views here.
from .models import *

from django.db.models import Q


def user_login(request):
    """登录界面"""
    context = {}
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        next_url = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # login log
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
                    if x_forwarded_for and x_forwarded_for[0]:
                        login_ip = x_forwarded_for[0]
                    else:
                        login_ip = request.META.get('REMOTE_ADDR', '')
                    user_agent = request.META.get('HTTP_USER_AGENT', '')
                    # write_login_log(request.user.username, ip=login_ip, user_agent=user_agent)
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect(reverse('dashboard'))
            else:
                context['error'] = '用户名或密码错误'
    return render(request, 'users/login.html', locals())


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:user-login'))


@login_required
def user_profile(request):
    app, action = '用户', '用户资料'
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('users:user_login'))
    return render(request, 'users/user_profile.html', locals())


@require_role(role='user')
def user_list(request, **kwargs):
    app, action = '用户', '用户列表'
    user_list = User.objects.all()
    return render(request, 'users/user_list.html', locals())


@require_role(role='admin')
def user_create(request):
    app, action = '用户', '创建用户'
    if request.method == 'GET':
        groups_selected = []
        return render(request, 'users/user_create_update.html', locals())

    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        is_superuser = request.POST.get('is_superuser', '')
        new_password = request.POST.get('new_password', '')
        verify_password = request.POST.get('verify_password', '')
        is_active = request.POST.get('is_active', '')
        try:
            if '' in [username, email, name, new_password, verify_password]:
                error = '带*内容不能为空'
                raise ServerError(error)
            if User.objects.filter(username=username):
                error = '用户名：%s 已存在' % username
                raise ServerError(error)
            if username in ['root', 'admin', 'administrator', 'superuser']:
                error = '用户名不能为: %s' % username
                raise ServerError(error)
            # if not re.match(r"^[A-Z,a-z][A-Z,a-z,0-9,_-]{4-16}$", username):
            #    error = '用户名不合法,用户名只可使用[a-z,A-Z,0-9,_-]中的字符,长度位4-16位'
            #    raise ServerError(error)
            if not (new_password == verify_password):
                error = '两次输入的密码不一致，请重新输入。'
                raise ServerError(error)
        except ServerError:
            pass
        else:
            user = User.objects.create(username=username, email=email, name=name, is_superuser=int(is_superuser),
                                       is_active=is_active)
            user.set_password(verify_password)
            user.save()
            msg = '添加用户成功'

    return render(request, 'users/user_create_update.html', locals())


@require_role(role='admin')
def user_delete(request):
    if request.method == "GET":
        user_id = request.GET.get('id', '')
        User.objects.filter(id=user_id).delete()
    return HttpResponseRedirect(reverse('users:user-list'))
