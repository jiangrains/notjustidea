# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

import json
import logging

from models import Account
from common.http_response_customer import HttpResponseCustomer
from common.errcode import *


# Create your views here.
@csrf_exempt
def signup(request):
	errCode = 0
	reason = []
	email = ""

	if request.method == "POST":
		email = request.POST.get("email", "")
		password = request.POST.get("password", "")
		captchaId = request.POST.get("captchaId", "")
		captcha = request.POST.get("captcha", "")

		logging.debug("email = %s password = %s captcha = %s." % (email, password, captcha))

		if email == "" or password == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":email})
		else:

			# TODO check captcha.

			if (Account.objects.filter(email=email).exists()):
				return HttpResponseCustomer(errCode = EMAIL_REPEAT_CODE, reason = [EMAIL_REPEAT], data = {"email":email})
			else:
				#account = Account.objects.create()
				#account = Account(email=email, password=password)
				#account.save()
				code = Account.objects.add_account(email = email, password = password)

				subject, from_email, to = 'others', 'jiangrains@126.com', 'jiangdunchuan2006@126.com'
				text_content = 'This is an important message.'
				html_content = '<b>激活链接：</b><a href="http://www.baidu.com?code=%s&email=%s">activate</a>' % (code, email)
				#html_content = '<p>This is an <strong>important</strong> message.</p>'
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":email})

	data = {}
	data["email"] = email
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")


@csrf_exempt
def signin(request):
	errCode = 0
	reason = []
	token = ""

	if request.method == "POST":
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		remember = request.POST.get("remember", None)
		token = ""

		#TODO check captcha.

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("USERNAME_OR_PASSWORD_INVALID")
		else:
			if account.password != password:
				errCode = 0x2
				reason.append("PASSWORD_INVALID")
			else:
				token = account.signin(remember)
				
	data = {}
	data["token"] = token
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")



@csrf_exempt
def checktoken(request):
	errCode = 0
	reason = []
	token = ""

	if request.method == "POST":
		token = request.POST.get("token", None)

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("USERNAME_OR_PASSWORD_INVALID")
		else:
			if account.password != password:
				errCode = 0x2
				reason.append("PASSWORD_INVALID")
			else:
				token = account.signin(remember)
				
	data = {}
	data["token"] = token
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")


@csrf_exempt
def activate(request):
	errCode = 0
	reason = []
	email = ""
	
	if request.method == "POST":
		email = request.POST.get("email", None)
		code = request.POST.get("code", None)

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("ACCOUNT_INVALID")
		else:
			if account.status == 0:
				account.activate(code)
			else:
				errCode = 0x2
				reason.append("ACCOUNT_DUP_ACTIVATED")
				
	data = {}
	data["email"] = email
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")


@csrf_exempt
def exists(request):
	errCode = 0
	reason = []
	exists = False
	
	if request.method == "GET":
		email = request.GET.get("email", None)

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("ACCOUNT_INVALID")
		else:
			exists = True
				
	data = {}
	data["exists"] = exists
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")

@csrf_exempt
def retrieve(request):
	errCode = 0
	reason = []
	email = ""

	if request.method == "GET":
		email = request.GET.get("email", None)
		captchaId = request.GET.get("captchaId", None)
		captcha = request.GET.get("captcha", None)

		# TODO check captcha.

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("ACCOUNT_INVALID")
		else:
			account.retrieve()

			subject, from_email, to = 'others', 'jiangrains@126.com', 'jiangdunchuan2006@126.com'
			text_content = 'This is an important message.'
			html_content = '<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
			#html_content = '<p>This is an <strong>important</strong> message.</p>'
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

	data = {}
	data["email"] = email
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")


@csrf_exempt
def resetpsw(request):
	errCode = 0
	reason = []
	
	if request.method == "GET":
		email = request.GET.get("email", None)
		code = request.GET.get("code", None)
		password = request.GET.get("password", None)

		try:
			account = Account.objects.get(email = email)
		except :
			errCode = 0x1
			reason.append("ACCOUNT_INVALID")
		else:
			account.resetpsw(code, password)
				
	data = {}
	response_data = {}
	response_data["v"] = "1.0"
	response_data["code"] = errCode
	response_data["reason"] = reason
	response_data["data"] = data
	return HttpResponse(json.dumps(response_data), content_type = "application/json")	



@csrf_exempt
def login(request):
	username = request.POST.get("username", None)
	password = request.POST.get("password",None)
	method = request.POST.get("method", None)
	invalid = request.POST.get("invalid", None)

	logging.debug("username:%s password:%s method:%s invalid:%s" % (username, password, method, invalid))

	if invalid == None:
		logging.debug("invalid is none.")
	else:
		logging.debug("invalid is not none.")

	if method == "1":
		Account.objects.add_account(username, password)
		logging.debug("succeed to add account.")
	elif method == "2":
		try:
			entry = Account.objects.get(username = username)
		except Exception,e:
			logging.debug("Exception for getting user=%s", username)
		#entries = Account.objects.filter(username = username)
		#entry = entries[0]
		#logging.debug("entries:%s entry[0]:%s" % (entries, entry.username))
		#Account.objects.find_account(username)


	response_data = {}
	response_data["username"] = "jiangdunchuan"
	response_data["password"] = "309Jiang"

	return HttpResponse(json.dumps(response_data), content_type = "application/json")
