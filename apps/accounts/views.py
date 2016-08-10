from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from models import Account


# Create your views here.

def signup(request):
	errCode = 0
	if request.method == "POST":
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		captchaId = request.POST.get("captchaId", None)
		captcha = request.POST.get("captcha", None)

		# TODO check captcha.

		if (Account.objects.filter(email=email).exists()):
			errCode = 0x1
		else:
			account = Account.objects.create()
			account = Account()
			account.save()
			





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
