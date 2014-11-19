from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
from rj2 import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.homepage, name="rj2_homepage"),
    url(r'^about', views.aboutus, name="rj2_aboutus"),
    url(r'^manage_courses/$', views.manage_courses, name='manage_courses'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/$', views.edit_course,
        name='edit_course'),
    url(r'^manage_courses/new/$', views.add_course, name='add_course'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/add_quiz/$',
        views.add_quiz, name='add_quiz'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/quiz_list/$',
        views.quiz_list, name='quiz_list'),
    url(r'^edit_quiz/(?P<pk>[0-9]+)/$',
        views.edit_quiz, name='edit_quiz'),
    url(r'^edit_quiz/(?P<pk>[0-9]+)/add_question/$',
        views.add_question, name="add_question"),
    url(r'^edit_quiz/(?P<pk>[0-9]+)/question_list/$',
        views.question_list, name="question_list"),
    url(r'^edit_question/(?P<pk>[0-9]+)/$',
        views.edit_question, name="edit_question"),
    url(r'^edit_question/(?P<pk>[0-9]+)/add_answer/$',
        views.add_answer, name="add_answer"),
    url(r'^edit_question/(?P<pk>[0-9]+)/answer_list/$',
        views.answer_list, name="answer_list"),
    url(r'^edit_answer/(?P<pk>[0-9]+)/$',
        views.edit_answer, name='edit_answer'),
    url(r'^take_quiz/(?P<pk>[0-9]+)/$',
        views.take_quiz, name="take_quiz"),
)
