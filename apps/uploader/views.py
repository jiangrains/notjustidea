from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm


# Create your views here.

@csrf_exempt
def upload(request):
	if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
	return HttpResponseRedirect('/static/login.html')
