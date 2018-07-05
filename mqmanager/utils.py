# -*- coding:utf8 -*-
from __future__ import unicode_literals
import logging
import urllib
import urllib2
import json
from settings import rabbitmq_list


class RabbitMQAPI(object):
    '''Class for RabbitMQ Management API'''

    def __init__(self, host_name='192.168.2.12', user_name='guest', password='guest', port=15672, protocol='http',
                 queue_name=''):
        self.user_name = user_name
        self.password = password
        self.port = port
        self.protocol = protocol or 'http'
        self.queue_name = queue_name
        self.host_name = host_name

    def call_api(self, method='GET', path='', data=''):
        '''Call the REST API and convert the results into JSON.'''
        url = '{0}://{1}:{2}/api/{3}'.format(self.protocol, self.host_name, self.port, path)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.user_name, self.password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        # logging.debug('Issue a rabbit API call to get data on ' + path + " against " + self.host_name)
        # logging.debug('Full URL:' + url)
        print(url, method, data)
        if method == 'PUT':
            request = urllib2.Request(url, data=data)
            request.add_header('content-type', 'application/json')
            request.get_method = lambda: 'PUT'
            return urllib2.build_opener(handler).open(request)
        if method == 'POST':
            request = urllib2.Request(url, data=data)
            request.add_header('content-type', 'application/json')
            request.get_method = lambda: 'POST'
            return urllib2.build_opener(handler).open(request)
        if method == 'DELETE':
            request = urllib2.Request(url, data=data)
            request.add_header('content-type', 'application/json')
            request.get_method = lambda: 'DELETE'
            return urllib2.build_opener(handler).open(request)
        return json.loads(urllib2.build_opener(handler).open(url).read())

    def list_vhosts(self, filters=None):
        res = self.call_api(path='vhosts')
        return res

    def create_vhost(self, vhost):
        try:
            self.call_api(method='PUT', path='/vhosts/%s' % urllib.quote_plus(vhost))
            message = {'tags': 'success', 'detail': '创建虚拟主机成功', 'obj': vhost}
        except Exception, e:
            message = {'tags': 'danger', 'detail': '创建虚拟主机失败:%s' % e, 'obj': vhost}
        return message

    def delete_vhost(self, vhost):
        res = self.call_api(method='DELETE', path='vhosts/%s' % urllib.quote_plus(vhost))
        return res

    def list_permission(self, vhost):
        res = self.call_api(path='vhosts/%s/permissions' % urllib.quote_plus(vhost))
        return res

    def create_permission(self, vhost, user):
        try:
            self.call_api(method='PUT', path='permissions/%s/%s' % (vhost, user))
            message = {'tags': 'success', 'detail': '添加权限成功'}
        except Exception, e:
            message = {'tags': 'success', 'detail': '添加权限失败'}
        return message

    def list_users(self):
        return self.call_api(path='users')

    def list_queues(self, vhost=''):
        res = self.call_api(path='queues/' + urllib.quote_plus(vhost))
        return res

    def create_queue(self, vhost='v1', queue='', data={}):
        try:
            self.call_api(method='PUT', path='queues/%s/%s' % (urllib.quote_plus(vhost), queue),
                          data=json.dumps(data))
            message = {'tags': 'success', 'detail': '创建队列成功', 'obj': queue}
        except Exception, e:
            message = {'tags': 'danger', 'detail': '创建队列失败:%s' % e, 'obj': queue}
        return message

    def delete_queue(self, vhost, queue):
        res = self.call_api(method='DELETE', path='queues/%s/%s' % (urllib.quote_plus(vhost), urllib.quote_plus(queue)))
        return res

    def list_exchanges(self):
        res = self.call_api(path='exchanges')
        return res

    def create_exchange(self, vhost, exchange, data={}):
        try:
            self.call_api(method='PUT',
                          path='exchanges/%s/%s' % (urllib.quote_plus(vhost), urllib.quote_plus(exchange)),
                          data=json.dumps(data))
            message = {'tags': 'success', 'detail': '创建交换机成功'}
        except Exception, e:
            message = {'tags': 'danger', 'detail': '创建交换机失败:%s' % e}
        return message

    def delete_exchange(self, vhost, exchange, data={}):
        res = self.call_api(method='DELETE',
                            path='exchanges/%s/%s' % (urllib.quote_plus(vhost), urllib.quote_plus(exchange)),
                            data=json.dumps(data))
        return res

    def list_bindings(self, vhost, exchange):
        res = self.call_api(path='exchanges/%s/%s/bindings/source' % (urllib.quote_plus(vhost), exchange))
        return res

    def create_binding(self, vhost, exchange, type, destination, data={}):
        try:
            self.call_api(method='POST',
                          path='bindings/%s/e/%s/%s/%s' % (urllib.quote_plus(vhost), exchange, type, destination),
                          data=json.dumps(data))
            message = {'tags': 'success', 'detail': '绑定到交换机成功'}
        except urllib2.URLError, e:
            message = {'tags': 'danger', 'detail': '绑定到交换机失败:%s' % e.reason}

        return message

    def delete_binding(self, vhost, exchange, type, destination, properties_key, data={}):
        try:
            self.call_api(method='DELETE',
                          path='bindings/%s/e/%s/%s/%s/%s' % (
                              urllib.quote_plus(vhost), exchange, type, destination, properties_key),
                          data=json.dumps(data))
            return True
        except urllib2.URLError, e:
            return e.reason


'''
http://192.168.2.12:15672/api/bindings/%2F/e/e1/q/q1
{"vhost":"/","source":"e1","destination_type":"q","destination":"q1","routing_key":"PROCESS1","arguments":{}}
http://192.168.2.12:15672/api/bindings/%2F/e/E_PAY_PAYMENT_NOTIFY/q/BLPAY_BIZ_MERCHANT_APPLY_QUEUE
binding:{"vhost":"/","source":"E_PAY_PAYMENT_NOTIFY","destination_type":"q","destination":"BLPAY_BIZ_MERCHANT_APPLY_QUEUE","routing_key":"PROCESS1","arguments":{}}

http://192.168.2.12:15672/api/bindings/%2F/e/E_PAY_PAYMENT_NOTIFY/e/E_PAY_ANTIFRAUD_LOCAL
{"vhost":"/","source":"E_PAY_PAYMENT_NOTIFY","destination_type":"e","destination":"E_PAY_ANTIFRAUD_LOCAL","routing_key":"PROCESS2","arguments":{}}

delete binding
http://192.168.2.12:15672/api/bindings/%2F/e/e1/q/qqq1/rtk11
{"vhost":"/","source":"e1","destination":"qqq1","destination_type":"q","properties_key":"rtk11"}
'''
a = RabbitMQAPI()


# a.delete_binding(vhost='/', exchange='e1', type='q', destination='qqq1', properties_key='rtk11',
#                 data={"vhost": "/", "source": "e1", "destination": "qqq1", "destination_type": "q",
#                      "properties_key": "rtk11"})


# a.create_binding('/','e1','q','q1',data={"vhost":"/","source":"e1","destination_type":"q","destination":"q1","routing_key":"PROCESS1","arguments":{}})
# a.create_binding('/','e1','e','e1',data={"vhost":"/","source":"e1","destination_type":"e","destination":"e1","routing_key":"PROCESS1","arguments":{}})
# a.create_binding('/','e1','e','e2',data={"vhost":"/","source":"e1","destination_type":"e","destination":"e2","routing_key":"PROCESS1","arguments":{}})

# a.create_exchange('csdnpay', 'csdnpay_e2',{"vhost":"csdnpay","name":"csdnpay_e2","type":"fanout","durable":"true","auto_delete":"false","internal":"false","arguments":{"alternate-exchange":"E_PAY_TRADE_LOCAL"}})


# a.delete_queue('csdnpay', 'csdnpay_q11')
# a.delete_vhost('test5')
# a.create_queue(vhost='/', queue='q9')
# /api/queues/vhost/name
# /api/queues/vhost/name
# http://192.168.2.12:15672/api/queues/csdnpay/csdnpay_q8
# (u'http://192.168.2.12:15672/api/queues/csdnpay/csdnpay_q11', u'PUT', '{"vhost": "csdnpay", "durable": "true", "name": "csdnpay_q11", "auto_delete": "false", "arguments": {}}')
class batch_exec(RabbitMQAPI):
    def __init__(self, cluster_selected=rabbitmq_list):
        self.cluster_all = rabbitmq_list
        self.cluster = {k: v for k, v in self.cluster_all.items() if k in cluster_selected}
        cluster_connector_args = {}
        for k, v in self.cluster.items():
            cluster_name = k
            protocol = v['api_url'].split(':')[0]
            host_name = v['api_url'].split(':')[1].replace('/', '')
            port = int(v['api_url'].split(':')[2])
            user_name = v['username']
            password = v['password']
            cluster_connector_args[cluster_name] = {'protocol': protocol, 'host_name': host_name,
                                                    'port': port, 'user_name': user_name,
                                                    'password': password}
        self.cluster_connector_args = cluster_connector_args

    def list_vhosts(self):
        vhost_info = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            vhost_info.append({k: mq_obj.list_vhosts()})
        return vhost_info

    def create_vhost(self, vhost):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_vhost(vhost)
            res['detail'] = '[集群:%s][详情:%s][操作对象:%s]' % (k, res['detail'], res['obj'])
            messages.append(res)
        return messages

    def delete_vhost(self, vhost):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            mq_obj.delete_vhost(vhost)
        return True

    def list_permission(self, vhost):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
        return mq_obj.list_permission(vhost)

    def create_permission(self, vhost, user, data={}):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_permission(vhost, user)
            res['detail'] = '[集群:%s][详情:%s][操作对象:添加用户:%s操作虚拟主机:%s的权限:配置:%s,读:%s,写:%s]' % (
                k, res['detail'], user, vhost, data['config'], data['read'], data['write'])
            messages.append(res)
        return messages

    def list_users(self):
        user_info = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            user_info.append({k: mq_obj.list_users()})
        return user_info

    def list_queues(self, vhost=''):
        queue_info = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            queue_info.append({k: mq_obj.list_queues(vhost)})
        return queue_info

    def create_queue(self, vhost='/', queue='', data={}):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_queue(vhost=vhost, queue=queue, data=data)
            res['detail'] = '[集群:%s][详情:%s][操作对象:%s]' % (k, res['detail'], res['obj'])
            messages.append(res)
        return messages

    def delete_queue(self, vhost, queue):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            mq_obj.delete_queue(vhost, queue)
        return True

    def list_exchanges(self):
        exchange_info = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            exchange_info.append({k: mq_obj.list_exchanges()})
        return exchange_info

    def delete_exchange(self, vhost, exchange):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            mq_obj.delete_exchange(vhost, exchange, data={"vhost": vhost, "name": exchange})
        return True

    def create_exchange(self, vhost='/', exchange='', data={}):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_exchange(vhost=vhost, exchange=exchange, data=data)
            res['detail'] = '[集群:%s][详情:%s][操作对象:%s]' % (k, res['detail'], exchange)
            messages.append(res)
        return messages

    def list_bindings(self, vhost, exchange):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            binding_info = {k: mq_obj.list_bindings(vhost, exchange)}
        return binding_info

    def create_binding(self, vhost, exchange, type, destination, data={}):
        messages = []
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            res = mq_obj.create_binding(vhost, exchange, type, destination, data=data)
            res['detail'] = '[集群:%s][详情:%s][虚拟主机:%s][源交换机:%s][目标:%s][目标类型:%s]' % (
                k, res['detail'], vhost, exchange, destination, type)
            messages.append(res)
        return messages

    def delete_binding(self, vhost, exchange, type, destination, properties_key, data={}):
        for k, v in self.cluster_connector_args.items():
            mq_obj = RabbitMQAPI(protocol=v['protocol'], host_name=v['host_name'], port=v['port'],
                                 user_name=v['user_name'], password=v['password'])
            mq_obj.delete_binding(vhost, exchange, type, destination, properties_key, data=data)
        return True


'''
http://192.168.2.12:15672/api/bindings/%2F/e/E_PAY_PAYMENT_NOTIFY/q/BLPAY_BIZ_MERCHANT_APPLY_QUEUE
binding:{"vhost":"/","source":"E_PAY_PAYMENT_NOTIFY","destination_type":"q","destination":"BLPAY_BIZ_MERCHANT_APPLY_QUEUE","routing_key":"PROCESS1","arguments":{}}
        {'source': u'csdnpay_ee2', 'destination': u'csdnpay_q1', 'routing_key': u'rtkk', 'vhost': u'csdnpay', 'arguments': {}, 'destination_type': u'q'}

http://192.168.2.12:15672/api/bindings/%2F/e/E_PAY_PAYMENT_NOTIFY/e/E_PAY_ANTIFRAUD_LOCAL
{"vhost":"/","source":"E_PAY_PAYMENT_NOTIFY","destination_type":"e","destination":"E_PAY_ANTIFRAUD_LOCAL","routing_key":"PROCESS2","arguments":{}}


http://192.168.2.12:15672/api/exchanges/%2F/E_PAY_PAYMENT_NOTIFY/bindings/source

delete binding
http://192.168.2.12:15672/api/bindings/%2F/e/e1/q/qqq1/rtk11
{"vhost":"/","source":"e1","destination":"qqq1","destination_type":"q","properties_key":"rtk11"}
'''

# a = RabbitMQAPI(host_name='192.168.2.11')
# print(a.list_vhosts())
# print(a.list_exchanges())
# print(a.list_queues())
# print(a.create_vhosts('ssss1'))
# print(a.create_queue(queue='q2'))
# b = batch_exec()
# print(b.list_all_vhost())
# c= b.create_vhost(['shahem7','shahe'], 'ss')
# print(c)

# a = batch_exec()
# print(a.list_queues('csdnpay'))
# a.list_all_vhost()
# print(a.cluster_connector_args)
