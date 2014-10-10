from django.http import HttpResponse

def logout():
	return HttpResponse("You have successfully logged out of the Application")
	
def homepage():
	return HttpResponse("Homepage")
	
def editaccount():
	return HttpResponse("Edit Account")
	
def changepassword():
	return HttpResponse("Change Password")