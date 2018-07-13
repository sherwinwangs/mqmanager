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
                # if request.session.get('role_id', 0) < 2:
                if request.user.is_superuser == False:
                    return HttpResponseRedirect(reverse('dashboard'))
            return func(request, *args, **kwargs)

        return __deco

    return _deco
