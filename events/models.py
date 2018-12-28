# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""
备注事件以及今日要做事件
"""


class UserInfo(models.Model):
    """
    用户信息表
    """

    username = models.CharField(max_length=32,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=16)
    email = models.EmailField(unique=True,verbose_name="邮箱")
    avatar = models.FileField(upload_to="events/static/user/avatar",verbose_name="头像",null=True,blank=True)

    def __str__(self):
        return self.username


class Token(models.Model):
    """
    token 表
    """
    token = models.CharField(max_length=128,verbose_name="token")
    user = models.OneToOneField(to="UserInfo")


    def __str__(self):
        return "token:%s"%self.user


class ToDo(models.Model):
    """
    备注待做事件
    """
    title = models.CharField(max_length=64,verbose_name="备注名称")
    detail = models.TextField(verbose_name="事件详细")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user = models.ForeignKey("UserInfo",verbose_name="用户")
    type = models.ForeignKey("Type",verbose_name="事件类型")

    def __str__(self):
        return self.title


class Type(models.Model):
    """
    事件类型
    """
    title = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.title


class HaveToDo(models.Model):
    """
    今日需做事件
    """

    event = models.OneToOneField("ToDo")
    complete_choices = (
        (0,"完成"),
        (1,"未完成")
    )

    is_completed = models.SmallIntegerField(choices=complete_choices,default=1,verbose_name="是否完成")
    reason = models.CharField(max_length=512,verbose_name="未完成原因")
    completed_time = models.DateTimeField(null=True,blank=True,verbose_name="完成时间")
    summary = models.TextField(verbose_name="总结")

    def __str__(self):
        return self.event


