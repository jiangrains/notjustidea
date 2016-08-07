# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BankAccount(models.Model):
	name = models.CharField(max_length=256) #账户名称
	account = models.CharField(max_length=32) #账号
	bank = models.IntegerField() #开户行
	code = models.CharField(max_length=256) #不同国家和地区，其code含义不同


class Entiny(models.Model):
	nick = models.CharField(max_length=256)
	avatar = models.CharField(max_length=1024) #TODO待后续处理
	region = models.IntegerField()
	province = models.IntegerField()
	profile = models.CharField(max_length=1024) #TODO最大长度待后续处理
	site = models.CharField(max_length=256)
	bank_account = models.OneToOneField(BankAccount)
	type = models.IntegerField() #用户类型，0：individual，1：group，2：company

	def __unicode__(self):
   		return self.nick