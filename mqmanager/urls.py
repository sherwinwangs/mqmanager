"""mqmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    # cluster
    # url(r'cluster/list$', views.cluster_list, name='cluster-list'),
    # url(r'cluster/create$', views.cluster_create, name='cluster-create'),

    # dashboard
    url(r'^$', dashboard, name='dashboard'),

    # cluster
    url(r'^cluster/list$', cluster_list, name='cluster-list'),

    # vhosts
    url(r'^vhost/list$', vhost_list, name='vhost-list'),
    url(r'^vhost/add$', vhost_create, name='vhost-add'),
    url(r'^vhost/delete$', vhost_delete, name='vhost-delete'),

    # permission
    url(r'^permission/list$', permission_list, name='permission-list'),
    url(r'^permission/add$', permission_create, name='permission-add'),
    url(r'^permission/delete$', permission_delete, name='permission-delete'),

    # queue
    url(r'^queue/list$', queue_list, name='queue-list'),
    url(r'^queue/add$', queue_create, name='queue-add'),
    url(r'^queues/delete$', queue_delete, name='queue-delete'),

    # exchange
    url(r'^exchange/list$', exchange_list, name='exchange-list'),
    url(r'^exchange/add$', exchange_create, name='exchange-add'),
    url(r'^exchanges/delete$', exchange_delete, name='exchange-delete'),

    # binding
    url(r'^exchanges/bindings/list', binding_list, name='binding-list'),
    url(r'^exchange/bindings/add', binding_create, name='binding-add'),
    url(r'^exchange/bindings/delete', binding_delete, name='binding-delete'),

    # url(
    #    r'^mq/(?P<cluster>\w+)/bindings/(?P<vhost>[\s\S]*)/e/(?P<exchange>[\s\S]*)/(?P<type>[\s\S]*)/(?P<destination>[\s\S]*)/(?P<properties_key>[\s\S]*)/delete$',
    #    binding_delete,
    #    name='binding-delete'),
    # (vhost, exchange, type, destination, properties_key, data)
    url(r'^testurl$', test_url,
        name='test-url'),
]
