# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import User

class AccountManager(models.Manager):

    def add_account(self, username, password):
        account = self.model(username = username, password = password) #创建account实例
        account.save() #将实例写入数据库


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=256) #注册邮箱
    password = models.CharField(max_length=256)
    status = models.IntegerField() #账号状态，0：未激活，1：正常，2：其他状态
    phone = models.CharField(max_length=32) #若绑定手机，则为手机号；否则为空
    signup_date = models.DateTimeField(auto_now=False) #注册时间
    sign_in = models.DateTimeField(auto_now=False) #最后登录时间
    code = models.CharField(max_length=256) #激活码
    code_expire_date = models.DateTimeField(auto_now=False) #激活码过期时间
    token = models.CharField(max_length=256) #令牌
    token_expire_date = models.DateTimeField(auto_now=False) #令牌过期时间
    objects = AccountManager() #重写Account的管理器

    def __unicode__(self):
        return self.username





