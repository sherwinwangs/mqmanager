# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


# Create your models here.

class QueueInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255, unique=False, verbose_name="队列名称")
    consumers = models.CharField(max_length=255, unique=False, verbose_name="消费者集群")
    comment = models.CharField(max_length=255, null=True, verbose_name="描述信息")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
