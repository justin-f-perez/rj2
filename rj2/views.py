from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login_required

def logout(request):
	return HttpResponse("You have successfully logged out of the Application")
	
@login_required
def homepage(request):
	return HttpResponse("Homepage")
