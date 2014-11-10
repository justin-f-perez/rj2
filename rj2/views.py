from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from rj2.forms import CourseForm
from rj2.models import Course, Quiz

def aboutus(request):
    return render(request, "rj2/about.html")

@login_required
def homepage(request):
	return render(request, "rj2/index.html")


@login_required
def manage_courses(request):
    form_class = CourseForm
    form = form_class()
    courses = Course.objects.filter(content_manager=request.user)
    return render(request, "rj2/deleteCourse.html", 
                  {"form": form, "courses": courses})


class CourseUpdate(UpdateView):
    model = Course
    fields = ['name', 'description', 'fee', 'is_deprecated', 'is_active',
              'instructors']
    success_url = '/manage_courses'


edit_course = login_required(CourseUpdate.as_view())

@login_required
def add_course(request):
    form_class = CourseForm
    template_name = 'rj2/addCourse.html'

    if request.method == 'POST':
        form = form_class(request.POST)
        form.instance.content_manager = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
        else:
            return render(request, template_name, {'form': form})
    else:
        form = form_class()
        return render(request, template_name, {'form': form})

class QuizCreate(CreateView):
    model = Quiz
    fields = ['title',]

    def dispatch(self, pk, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=pk)
        return super().dispatch(*args, **kwargs)

add_quiz = login_required(QuizCreate.as_view())

class QuizUpdate(UpdateView):
    model = Quiz
    fields = ['title']
    success_url = '/manage_courses'

edit_quiz = login_required(QuizUpdate.as_view())
