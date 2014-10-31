from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from rj2.forms import CourseForm

def logout(request):
	return HttpResponse("You have successfully logged out of the Application")
	
@login_required
def homepage(request):
	return HttpResponse("Homepage")


def manage_courses(request):
	return HttpResponse("Manage Courses")


def edit_course(request, pk=None):
	return HttpResponse("Edit Courses")


def add_course(request):
    form_class = CourseForm
    render_to_response("addCourse.html", {'form': form_class())
