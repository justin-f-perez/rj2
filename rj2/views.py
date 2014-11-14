from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from rj2.forms import CourseForm
from rj2.models import Course, Quiz, Answer, Question

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
    success_url = '/manage_courses'

    def dispatch(self, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.course = self.course
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

add_quiz = login_required(QuizCreate.as_view())

class QuizUpdate(UpdateView):
    model = Quiz
    fields = ['title']
    success_url = '/manage_courses'

edit_quiz = login_required(QuizUpdate.as_view())

class QuestionCreate(CreateView):
    model = Question
    fields = ['text']

    def get_success_url(self):
        return "/edit_question/" + str(self.object.pk) + "/add_answer/"
        #return reverse('add_answer', kwargs={'pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.quiz = self.quiz
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


add_question = login_required(QuestionCreate.as_view())


class QuestionUpdate(UpdateView):
        model = Question
        fields = ['text', 'answers']

        def get_success_url(self):
            return "/edit_question/" + str(self.object.pk) + "/"


edit_question = login_required(QuestionUpdate.as_view())


class AnswerCreate(CreateView):
    model = Answer
    fields = ['text']

    def dispatch(self, *args, **kwargs):
        self.question= get_object_or_404(Question, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.question
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/edit_question/" + str(self.question.pk) + "/add_answer/"

add_answer = login_required(AnswerCreate.as_view())
edit_answer = login_required(UpdateView.as_view(model=Answer))
