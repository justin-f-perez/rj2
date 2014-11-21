from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, TemplateView, View
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
    template_name = 'rj2/editCourse.html'
	


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


class QuizMixin(View):
    model = Quiz
    fields = ['title']
    
    def dispatch(self, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['course'] = self.course
        return context


class QuizCreate(QuizMixin, CreateView):
    success_url = '/manage_courses'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.course = self.course
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class QuizUpdate(QuizMixin, UpdateView):
    success_url = '/manage_courses'


class QuizList(QuizMixin, ListView):
    template = 'rj2/quiz_list.html'

    def get_queryset(self, *args, **kwargs):
        return Quiz.objects.filter(course=self.course)


class QuestionMixin(View):
    model = Question
    fields = ['text']

    def dispatch(self, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['quiz'] = self.quiz
        return context


class QuestionCreate(QuestionMixin, CreateView):
    def get_success_url(self):
        return "/edit_question/" + str(self.object.pk) + "/add_answer/"
        #return reverse('add_answer', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.quiz = self.quiz
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class QuestionUpdate(QuestionMixin, UpdateView):
        def get_success_url(self):
            return "/edit_question/" + str(self.object.pk) + "/"


class QuestionList(QuestionMixin, ListView):
    template = 'rj2/question_list.html'

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(quiz=self.quiz)


class AnswerMixin(View):
    model = Answer
    fields = ['text', 'is_correct']

    def dispatch(self, *args, **kwargs):
        self.question= get_object_or_404(Question, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['question'] = self.question
        return context


class AnswerCreate(AnswerMixin, CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.question
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/edit_question/" + str(self.question.pk) + "/add_answer/"


class AnswerUpdate(AnswerMixin, UpdateView):
    def get_successs_url(self):
        return "/edit_question/" + str(self.question.pk) + "/"


class AnswerList(AnswerMixin, ListView):
    template = 'rj2/answer_list.html'

    def get_queryset(self, *args, **kwargs):
        return Answer.objects.filter(question=self.question)


class TakeQuiz(TemplateView):
    template_name = 'rj2/take_quiz.html'

    def dispatch(self, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['quiz'] = self.quiz
        questions = Question.objects.filter(quiz=self.quiz)
        qdict = dict()
        for i in range(len(questions)):
            qdict['question'+str(i)] = questions[i].answers
        context['questions'] = qdict
        return context

    def post(self, request, *args, **kwargs):
        pass # BUG: need to process form data



add_answer = login_required(AnswerCreate.as_view())
edit_answer = login_required(AnswerUpdate.as_view())
answer_list = login_required(AnswerList.as_view())
edit_question = login_required(QuestionUpdate.as_view())
add_question = login_required(QuestionCreate.as_view())
question_list = login_required(QuestionList.as_view())
add_quiz = login_required(QuizCreate.as_view())
edit_quiz = login_required(QuizUpdate.as_view())
quiz_list = login_required(QuizList.as_view())
edit_course = login_required(CourseUpdate.as_view())
take_quiz = login_required(TakeQuiz.as_view())
