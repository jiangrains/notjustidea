# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

import json
import logging

from models import Account


# Create your views here.
@csrf_exempt
def signup(request):
	errCode = 0
	reason = []
	if request.method == "POST":
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		captchaId = request.POST.get("captchaId", None)
		captcha = request.POST.get("captcha", None)

		# TODO check captcha.

		if (Account.objects.filter(email=email).exists()):
			errCode = 0x1
			reason.append("EMAIL_REPEAT")
		else:
			#account = Account.objects.create()
			#account = Account(email=email, password=password)
			#account.save()
			Account.objects.add_account(email = email, password = password)

			subject, from_email, to = 'others', 'jiangrains@126.com', 'jiangdunchuan2006@126.com'
			text_content = 'This is an important message.'
			html_content = '<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
			#html_content = '<p>This is an <strong>important</strong> message.</p>'
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			#send_mail("other", 'helloworld', 'jiangrains@126.com', ['420286835@qq.com'], fail_silently=False)

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
	if request.method == "POST":
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		remember = request.POST.get("remember", None)

		#TODO check captcha.

		
			





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
