from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
from rj2 import views
from rj2 import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.homepage, name="rj2_homepage"),
    url(r'^about', views.aboutus, name="rj2_aboutus"),
    #course admin
    url(r'^manage_courses/$', views.manage_courses, name='manage_courses'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/$', views.edit_course,
        name='edit_course'),
    url(r'^manage_courses/new/$', views.add_course, name='add_course'),
    #quiz admin
    url(r'^manage_courses/(?P<pk>[0-9]+)/add_quiz/$',
        views.add_quiz, name='add_quiz'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/quiz_list/$',
        views.quiz_list, name='quiz_list'),
    url(r'^edit_quiz/(?P<pk>[0-9]+)/$',
        views.edit_quiz, name='edit_quiz'),
    #question admin
    url(r'^edit_quiz/(?P<pk>[0-9]+)/add_question/$',
        views.add_question, name="add_question"),
    url(r'^edit_quiz/(?P<pk>[0-9]+)/question_list/$',
        views.question_list, name="question_list"),
    url(r'^edit_question/(?P<pk>[0-9]+)/$',
        views.edit_question, name="edit_question"),
    #answer admin
    url(r'^edit_question/(?P<pk>[0-9]+)/add_answer/$',
        views.add_answer, name="add_answer"),
    url(r'^edit_question/(?P<pk>[0-9]+)/answer_list/$',
        views.answer_list, name="answer_list"),
    url(r'^edit_answer/(?P<pk>[0-9]+)/$',
        views.edit_answer, name='edit_answer'),
    #course info
    url(r'^courses/$', views.course_list, name="course_list"),
    url(r'^registered_courses/$', views.registered_courses,
        name="registered_courses"),
    url(r'^courses/(?P<pk>[0-9]+)/register$', views.register_course,
        name='register_course'),
    url(r'^courses/(?P<pk>[0-9]+)/$', views.course_detail,
        name="course_detail"),
    #take quiz
    url(r'^take_quiz/(?P<pk>[0-9]+)/$',
        views.take_quiz, name="take_quiz"),
#    url(r'serve_pdf/(?P<pk>[0-9]+)/$', views.serve_pdf, name="serve_pdf"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

