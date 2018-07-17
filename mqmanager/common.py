# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, reverse, HttpResponseRedirect, render
from settings import LOGIN_URL


class AuthDecorator(object):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(AuthDecorator, self).dispatch(request, *args, **kwargs)


def require_role(role='user'):
    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('users:user-login'))
            elif role == 'admin':
                if request.user.role in ['Admin']:
                    return func(request, *args, **kwargs)
            elif role == 'operator':
                if request.user.role in ['Operator', 'Admin']:
                    return func(request, *args, **kwargs)
            elif role == 'user':
                if request.user.role in ['Operator', 'Admin', 'User']:
                    return func(request, *args, **kwargs)
            return render(request, '403.html')

        return __deco

    return _deco


class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass
