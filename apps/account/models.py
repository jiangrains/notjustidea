# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AccountManager(models.Manager):

    def add_account(self, username, password):
    	account = self.model(username = username, password = password) #创建account实例
    	account.save() #将实例写入数据库


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    objects = AccountManager() #重写Account的管理器

    def __unicode__(self):
    	return self.username





