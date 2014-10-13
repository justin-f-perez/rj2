from django.http import HttpResponse
from django.shortcuts import render

def logout(request):
	return HttpResponse("You have successfully logged out of the Application")
	
def homepage(request):
	return HttpResponse("Homepage")
	
def editaccount(request):
	return HttpResponse("Edit Account")
	
def changepassword(request):
	return HttpResponse("Change Password")