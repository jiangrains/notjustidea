# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import User

import django.utils.timezone as timezone
import datetime

class Utils():
    def get_random_string(len):
        return ''.join(random.sample(string.ascii_letters + string.digits, len))  


class AccountManager(models.Manager):

    def add_account(self, email, password):
        account = self.model(email = email, password = password) #创建account实例
        account.save() #将实例写入数据库


# Create your models here.
class Account(models.Model):
    ACCOUNT_NOTACTIVE = 0
    ACCOUNT_ACTIVE = 1
    ACCOUNT_LOCKED = 2

    TOKEN_EXPIRE_DAYS = (2*7) #2 weeks
    
    #user = models.OneToOneField(User)
    email = models.CharField(max_length = 256) #注册邮箱
    password = models.CharField(max_length = 256)
    status = models.IntegerField(default = ACCOUNT_NOTACTIVE) #账号状态，0：未激活，1：正常，2：其他状态
    phone = models.CharField(max_length = 32) #若绑定手机，则为手机号；否则为空
    signup_date = models.DateTimeField(auto_now_add = True) #注册时间 (import django.utils.timezone as timezone ; default = timezone.now)
    signin_date = models.DateTimeField(auto_now = True) #最后登录时间
    code = models.CharField(max_length = 256) #激活码
    code_expire_date = models.DateTimeField(default = timezone.now) #激活码过期时间
    token = models.CharField(max_length = 256) #令牌
    token_expire_date = models.DateTimeField(default = timezone.now) #令牌过期时间
    objects = AccountManager() #重写Account的管理器

    def __unicode__(self):
        return self.username

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        #user = None

    def remember(self, remember):
        if remember == True:
            self.token = Utils.get_random_string(32)
            self.token_expire_date = timezone.now + datetime.timedelta(days = TOKEN_EXPIRE_DAYS)
        else:
            self.token = ""
        return self.token    

            





