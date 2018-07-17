# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid


# Create your models here.


class User(AbstractUser):
    ROLE_ADMIN = 'Admin'
    ROLE_OPERATOR = 'Operator'
    ROLE_USER = 'User'

    ROLE_CHOICES = (
        (ROLE_ADMIN, '超级管理员'),
        (ROLE_OPERATOR, '队列管理员'),
        (ROLE_USER, '普通用户')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, null=True, verbose_name='姓名')
    # avatar = models.ImageField(upload_to="avatar", null=True, verbose_name='头像')
    wechat = models.CharField(max_length=128, null=True, verbose_name='微信')
    phone = models.CharField(max_length=20, null=True, verbose_name='手机')
    date_expired = models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间')
    created_by = models.CharField(max_length=30, default='', verbose_name='创建者')
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_USER, max_length=10,
                            verbose_name='用户角色')
    comment = models.TextField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.name
