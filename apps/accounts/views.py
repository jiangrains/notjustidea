# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

import json
import logging

from accounts.models import Account
from common.http_response_customer import HttpResponseCustomer
from common.views import check_captcha_inna
from common.errcode import *




# Create your views here.
@csrf_exempt
def signup(request):
	if request.method == "POST":
		email = request.POST.get("email", "")
		password = request.POST.get("password", "")
		captchaId = request.POST.get("captchaId", "")
		captcha = request.POST.get("captcha", "")

		if email == "" or password == "" or captchaId == "" or captcha == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":email})

		errCode, reason = check_captcha_inna(captchaId, captcha)
		if errCode != 0:
			return HttpResponseCustomer(errCode = errCode, reason = [reason], data = {"email":email})

		if (Account.objects.filter(email=email).exists()):
			return HttpResponseCustomer(errCode = EMAIL_REPEAT_CODE, reason = [EMAIL_REPEAT], data = {"email":email})
		else:
			#account = Account.objects.create()
			#account = Account(email=email, password=password)
			#account.save()
			code = Account.objects.add_account(email = email, password = password)

			subject, from_email, to = 'others', 'jiangrains@126.com', email
			text_content = 'This is an important message.'
			html_content = u"<b>激活链接：</b><a href=\"http://120.25.221.4/accounts/activate?code=%s&email=%s\">activate</a>" % (code, email)
			try:
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			except :
				return HttpResponseCustomer(errCode = EMAIL_SEND_FAIL_CODE, reason = [EMAIL_SEND_FAIL], data = {"email":email})
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":""})
	return HttpResponseCustomer(errCode = 0, reason = [], data = {"email":email})


@csrf_exempt
def signin(request):
	if request.method == "POST":
		email = request.POST.get("email", "")
		password = request.POST.get("password", "")
		remember = request.POST.get("remember", "")
		captchaId = request.POST.get("captchaId", "")
		captcha = request.POST.get("captcha", "")

		

		if email == "" or password == "" or remember == "" or captchaId == "" or captcha == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})
		remember = (remember == "true")	

		errCode, reason = check_captcha_inna(captchaId, captcha)
		if errCode != 0:
			return HttpResponseCustomer(errCode = errCode, reason = [reason], data = {})

		try:
			account = Account.objects.get(email = email)
		except :
			return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"token":""})
		else:
			if account.password != password:
				return HttpResponseCustomer(errCode = PASSWORD_INVALID_CODE, reason = [PASSWORD_INVALID], data = {"token":""})

			if account.status == Account.ACCOUNT_NOTACTIVATED:
				return HttpResponseCustomer(errCode = ACCOUNT_NOTACTIVATED_CODE, reason = [ACCOUNT_NOTACTIVATED], data = {"token":""})
			
			token = account.signin(remember)
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})
	return HttpResponseCustomer(errCode = 0, reason = [], data = {"token":token})



@csrf_exempt
def checktoken(request):
	token = request.POST.get("token", "")
	if request.method == "POST" and token != "":
		try:
			account = Account.objects.get(token = token)
		except :
			return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

	if account.checktoken() != 0:
		return HttpResponseCustomer(errCode = TOKEN_EXPIRE_CODE, reason = [TOKEN_EXPIRE], data = {"token":token})
	else:
		return HttpResponseCustomer(errCode = 0, reason = [], data = {"token":token})	



@csrf_exempt
def activate(request):
	if request.method == "GET":
		email = request.GET.get("email", "")
		code = request.GET.get("code", "")

		if email == "" or code == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":""})

		try:
			account = Account.objects.get(email = email)
		except :
			return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"email":email})
		else:
			if account.status != Account.ACCOUNT_NOTACTIVATED:
				return HttpResponseCustomer(errCode = ACCOUNT_ACTIVATED_CODE, reason = [ACCOUNT_ACTIVATED], data = {"email":email})

			if account.code != code:
				return HttpResponseCustomer(errCode = CODE_ILLEGAL_CODE, reason = [CODE_ILLEGAL], data = {"email":email, "code":code})

			account.activate()
			return HttpResponseCustomer(errCode = 0, reason = [], data = {"email":email})				
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":""})



@csrf_exempt
def exists(request):
	if request.method == "GET":
		email = request.GET.get("email", "")

		try:
			account = Account.objects.get(email = email)
		except :
			exists = False
		else:
			exists = True
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"exists":False, "email":""})
	return HttpResponseCustomer(errCode = 0, reason = [], data = {"exists":exists})




@csrf_exempt
def retrieve(request):
	if request.method == "GET":
		email = request.GET.get("email", "")
		captchaId = request.GET.get("captchaId", "")
		captcha = request.GET.get("captcha", "")

		if email == "" or captchaId == "" or captcha == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"sended":False})

		errCode, reason = check_captcha_inna(captchaId, captcha)
		if errCode != 0:
			return HttpResponseCustomer(errCode = errCode, reason = [reason], data = {"email":email})

		try:
			account = Account.objects.get(email = email)
		except :
			return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"sended":False})
		else:

			if account.status == Account.ACCOUNT_NOTACTIVATED:
				return HttpResponseCustomer(errCode = ACCOUNT_NOTACTIVATED_CODE, reason = [ACCOUNT_NOTACTIVATED], data = {"sended":False})

			code = account.retrieve()

			subject, from_email, to = 'others', 'jiangrains@126.com', email
			text_content = 'This is an important message.'
			html_content = u"<b>重置密码页面：</b><a href=\"http://www.baidu.com?code=%s&email=%s\">resetpsw</a>" % (code, email)
			try:
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			except :
				return HttpResponseCustomer(errCode = EMAIL_SEND_FAIL_CODE, reason = [EMAIL_SEND_FAIL], data = {"sended":False, "email":email})

			return HttpResponseCustomer(errCode = 0, reason = [], data = {"sended":True})
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"sended":False})



@csrf_exempt
def resetpsw(request):
	if request.method == "GET":
		email = request.GET.get("email", "")
		code = request.GET.get("code", "")
		password = request.GET.get("password", "")

		if email == "" or code == "" or password == "":
			return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"email":email, "code":code, "password":password})

		try:
			account = Account.objects.get(email = email)
		except :
			return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"email":email})
		else:
			if account.status == Account.ACCOUNT_NOTACTIVATED:
				return HttpResponseCustomer(errCode = ACCOUNT_NOTACTIVATED_CODE, reason = [ACCOUNT_NOTACTIVATED], data = {"email":email})

			if account.code != code:
				return HttpResponseCustomer(errCode = CODE_ILLEGAL_CODE, reason = [CODE_ILLEGAL], data = {"email":email, "code":code})

			account.resetpsw(password)
			return HttpResponseCustomer(errCode = 0, reason = [], data = {})
	else:
		return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})


@csrf_exempt
def delete(request):
	if request.method == "POST":
		email = request.POST.get("email", "")
		try:
			account = Account.objects.get(email = email)
		except :
			pass
		else:
			account.delete()

	return HttpResponseCustomer(errCode = 0, reason = [], data = {})


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


