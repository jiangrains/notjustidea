from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

# Create your views here.

@csrf_exempt
def login(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')

	logging.debug("username:%s password:%s" % (username, password))


	response_data = {}
	response_data['username'] = 'jiangdunchuan'
	response_data['password'] = '309Jiang'

	return HttpResponse(json.dumps(response_data), content_type = 'application/json')
