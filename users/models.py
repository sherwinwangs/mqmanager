# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, null=True, verbose_name='姓名')
    # avatar = models.ImageField(upload_to="avatar", null=True, verbose_name='头像')
    wechat = models.CharField(max_length=128, null=True, verbose_name='微信')
    phone = models.CharField(max_length=20, null=True, verbose_name='手机')
    date_expired = models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间')
    created_by = models.CharField(max_length=30, default='', verbose_name='创建者')
    comment = models.TextField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.name