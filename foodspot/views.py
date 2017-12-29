from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
@csrf_exempt
def testAuth(request):
	username = request.POST.get("username")
	password = request.POST.get("password")
	print username + " " + password
	user = authenticate(username=username, password=password)
	if not user == None:
		return HttpResponse("yes")
	else:
		return HttpResponse("No")