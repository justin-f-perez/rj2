from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rj2.forms import CourseForm
from rj2.models import Course


@login_required
def homepage(request):
	return render(request, "rj2/index.html")


@login_required
def manage_courses(request):
    form_class = CourseForm
    form = form_class()
    courses = Course.objects.all()
    return render(request, "rj2/deleteCourse.html", 
                  {"form": form, "courses": courses})


@login_required
def edit_course(request, pk=None):
    return HttpResponse("Manage Courses")


@login_required
def add_course(request):
    form_class = CourseForm
    template_name = 'rj2/addCourse.html'

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(template_name)
        else:
            return render(request, template_name, {'form': form})
    else:
        form = form_class()
        return render(request, template_name, {'form': form})
