# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import datetime
# Create your models here.


class Auditlog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    logtime = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    user = models.CharField(max_length=128, verbose_name='操作人')
    cluster = models.CharField(max_length=128,null=True, verbose_name='MQ集群')
    type = models.CharField(max_length=128, null=True, verbose_name='类型')
    target = models.CharField(max_length=128, null=True, verbose_name='对象')
    url = models.CharField(max_length=128, null=True, verbose_name='URL')
    method = models.CharField(max_length=128, null=True, verbose_name='参数')
    data = models.CharField(max_length=128, null=True, verbose_name='数据')
    comment = models.TextField(max_length=200, null=True,verbose_name='备注')

    def __str__(self):
        return self.url

    class Meta:
        ordering = ['-logtime']