from django.conf.urls import url
from .views import *

app_name = 'mq'

urlpatterns = [
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
    url(r'^queue/delete$', queue_delete, name='queue-delete'),
    url(r'^queue/detail$', queue_detail, name='queue-detail'),

    # exchange
    url(r'^exchange/list$', exchange_list, name='exchange-list'),
    url(r'^exchange/add$', exchange_create, name='exchange-add'),
    url(r'^exchanges/delete$', exchange_delete, name='exchange-delete'),

    # binding
    url(r'^exchanges/bindings/list$', binding_list, name='binding-list'),
    url(r'^exchange/bindings/add$', binding_create, name='binding-add'),
    url(r'^exchange/bindings/delete$', binding_delete, name='binding-delete'),

    # definitions
    url(r'^definitions/sync$', definitions_sync, name='definitions-sync'),
    url(r'^definitions/export$', definitions_export, name='definitions-export'),

    # audit log
    url(r'^audit$', audit_log, name='audit-log'),

    # queue for cluster
    url(r'^queue/cluster/sync', queue_cluster_sync, name='queue-cluster-sync'),
]
