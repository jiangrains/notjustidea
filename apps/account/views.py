from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

# Create your views here.

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


	response_data = {}
	response_data["username"] = "jiangdunchuan"
	response_data["password"] = "309Jiang"

	return HttpResponse(json.dumps(response_data), content_type = "application/json")
