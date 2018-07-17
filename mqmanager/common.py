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
                if not request.user.is_superuser:
                    return render(request, '403.html', locals())
            return func(request, *args, **kwargs)

        return __deco

    return _deco


class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass