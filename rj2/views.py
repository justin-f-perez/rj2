from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, TemplateView, View
from django.core.exceptions import PermissionDenied
from rj2.forms import CourseForm
from rj2.models import (Course, Quiz, Answer, Question, CourseRegistration,
                       Video, PDF, Score)
from reportlab.pdfgen import canvas
from django import forms

def aboutus(request):
    return render(request, "rj2/about.html")

@login_required
def homepage(request):
	return render(request, "rj2/index.html")


@login_required
def manage_courses(request):
    if request.user.is_content_manager or request.user.is_admin:    
        form_class = CourseForm
        form = form_class()
        courses = Course.objects.filter(content_manager=request.user)
        return render(request, "rj2/deleteCourse.html", 
              {"form": form, "courses": courses})
    else:
        raise PermissionDenied

		
class CourseUpdate(UpdateView):
    model = Course
    fields = ['name', 'description', 'fee', 'is_deprecated', 'is_active',
              'instructors']
    success_url = '/manage_courses'
    template_name = 'rj2/editCourse.html'

    def dispatch(self, request, *args, **kwargs):	
        self.course = Course.objects.get(pk=kwargs['pk'])
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        for key in request.FILES:
            f = request.FILES[key]
            pdf = PDF.objects.create(pdf_file=f, course=self.course)
        v = request.POST.get('video', False)
        if v:
            Video.objects.create(URL=v, course=self.course)
        
        return super().post(request=request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['videos'] = \
            Video.objects.filter(course=self.course)
        context['PDFs'] = \
            PDF.objects.filter(course=self.course)
        return context



@login_required
def add_course(request):
    form_class = CourseForm
    template_name = 'rj2/addCourse.html'

    permitted = request.user.is_content_manager or request.user.is_admin

    if not permitted:
        raise PermissionDenied

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['course'] = self.course
        return context


class QuizCreate(QuizMixin, CreateView):

    def get_success_url(self):
        return "/manage_courses/" + str(self.object.course.pk)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.course = self.course
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):	
        self.course = Course.objects.get(pk=kwargs['pk'])
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuizUpdate(QuizMixin, UpdateView):
    success_url = '/manage_courses'

    def dispatch(self, request, *args, **kwargs):	
        quiz = Quiz.objects.get(pk=kwargs['pk'])
        self.course = quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuizList(QuizMixin, ListView):
    template = 'rj2/quiz_list.html'

    def dispatch(self, request, *args, **kwargs):	
        self.course = Course.objects.get(pk=kwargs['pk'])
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self, *args, **kwargs):
        return Quiz.objects.filter(course=self.course)


class QuestionMixin(View):
    model = Question
    fields = ['text']

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

    def dispatch(self, request, *args, **kwargs):	
        self.quiz = Quiz.objects.get(pk=kwargs['pk'])
        self.course = self.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuestionUpdate(QuestionMixin, UpdateView):
    def get_success_url(self):
        return "/edit_question/" + str(self.object.pk) + "/"

    def dispatch(self, request, *args, **kwargs):	
        question = Question.objects.get(pk=kwargs['pk'])
        self.course = question.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuestionList(QuestionMixin, ListView):
    template = 'rj2/question_list.html'

    def dispatch(self, request, *args, **kwargs):	
        self.quiz = Quiz.objects.get(pk=kwargs['pk'])
        self.course = self.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(quiz=self.quiz)


class AnswerMixin(View):
    model = Answer
    fields = ['text', 'is_correct']

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

    def dispatch(self, request, *args, **kwargs):	
        self.question = Question.objects.get(pk=kwargs['pk'])
        self.course = self.question.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class AnswerUpdate(AnswerMixin, UpdateView):
    def get_successs_url(self):
        return "/edit_question/" + str(self.question.pk) + "/"

    def dispatch(self, request, *args, **kwargs):	
        answer = Answer.objects.get(pk=kwargs['pk'])
        self.course = answer.question.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied


class AnswerList(AnswerMixin, ListView):
    template = 'rj2/answer_list.html'

    def dispatch(self, request, *args, **kwargs):	
        self.question = Question.objects.get(pk=kwargs['pk'])
        self.course = self.question.quiz.course
        if request.user == self.course.content_manager or request.user.is_admin:
            return super().dispatch(request=request, *args, **kwargs)
        else:
            raise PermissionDenied

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
        questions = \
            Question.objects.filter(quiz=self.quiz).prefetch_related('answers')
        context['questions'] = questions
        return context

    def post(self, request, *args, **kwargs):
        CAN_RETAKE_QUIZZES = False
        questions = self.quiz.questions.all()
        total = len(questions)
        score = 0
        for question in questions:
            answer = request.POST.get("question_{}".format(question.id), None)
            if str(question.correct_answer_id) == str(answer):
                score += 1
        
        if CAN_RETAKE_QUIZZES:
            obj, created = Score.objects.update_or_create(user=request.user,
                    quiz=self.quiz, value=(score/total)*100)
        elif Score.objects.filter(user=request.user,
                    quiz=self.quiz).exists():
            raise Exception("Error: Cannot take the same quiz"
                        "multple times")
        else:
            Score.objects.create(user=request.user, quiz=self.quiz,
                    value=(score/total)*100)

        
        response = HttpResponseRedirect(reverse(course_detail,
            kwargs={'pk':self.quiz.course.id}))

        return response



class RegisteredCourseList(ListView):
    template_name = 'rj2/registered_course_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = \
            CourseRegistration.objects.filter(user=self.user).select_related('course')
        return qs

class CourseList(ListView):
    template_name = 'rj2/course_list.html'
    model = Course
	
    def get_queryset(self, *args, **kwargs):
        registered = CourseRegistration.objects.filter(user=self.user);
        courses = Course.objects.exclude(id__in=[c.id for c in registered]);
        return courses
		
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)
    
class CourseDetail(TemplateView):
    template_name = 'rj2/CourseInfo.html'

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(pk=kwargs['pk'])
        self.registration = \
            CourseRegistration.objects.get(user=request.user, course=self.course)
        print("Registration is complete? {}".format(self.registration.is_complete))
        self.incomplete_quizzes = []
        quizzes = Quiz.objects.filter(course=self.course)
        for quiz in quizzes:
            if not Score.objects.filter(user=request.user, quiz=quiz).exists():
                self.incomplete_quizzes.append(quiz)
        print("{}".format(self.incomplete_quizzes))
        
        return super().dispatch(request=request, *args, **kwargs)
		
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['course'] = self.course
        context['videos'] = \
            Video.objects.filter(course=self.course)
        context['PDFs'] = \
            PDF.objects.filter(course=self.course)
        context['quizzes'] = \
            Quiz.objects.filter(course=self.course)
        context['registration'] = self.registration
        context['incomplete_quizzes'] = self.incomplete_quizzes
        return context


@login_required
def register_course(request, pk):
    CourseRegistration.objects.create(user=request.user,
            course=Course.objects.get(pk=pk))
    return HttpResponseRedirect(reverse(course_list))

@login_required
def show_cert(request, course_id):
    course = Course.objects.get(pk=course_id)
    quizzes = Quiz.objects.filter(course=course)
    scores = []
    for quiz in quizzes:
        scores.extend(Score.objects.filter(user=request.user,
            quiz=quiz).all())
    score_list = ["{}%".format(s.value) for s in scores]
    score_string = ", ".join(score_list)

    response = HttpResponse(content_type='application/pdf')
    response['Certificate'] = 'attachment; filename="certificate.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Times-BoldItalic", 25)
    p.drawString(100, 700, "Congratulations!")
    p.setFont("Helvetica", 20)
    p.drawString(100, 650, request.user.email)
    p.drawString(100, 600, "You passed: ")
    p.drawString(220, 600, course.name)
    p.drawString(100, 550, "Quiz Scores: ")
    p.drawString(250, 550, score_string)
    p.showPage()
    p.save()
    return response

    
    


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
registered_courses = login_required(RegisteredCourseList.as_view())
course_list = login_required(CourseList.as_view())
course_detail = login_required(CourseDetail.as_view())
take_quiz = login_required(TakeQuiz.as_view())
