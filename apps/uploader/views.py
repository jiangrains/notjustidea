from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def upload(request):
	return HttpResponseRedirect('/static/login.html')