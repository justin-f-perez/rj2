from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
from django.views.generic.edit import CreateView
from rj2 import views
from rj2.models import Quiz

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.homepage, name="rj2_homepage"),
    url(r'^manage_courses/$', views.manage_courses, name='manage_courses'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/$', views.edit_course,
        name='edit_course'),
    url(r'^manage_courses/new/$', views.add_course, name='add_course'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/add_quiz/$',
        views.add_quiz, name='add_quiz'),
    url(r'^manage_courses/(?P<pk>[0-9]+)/add_quiz/(?P<quiz_id>[0-9]+)/$',
        views.edit_quiz, name='edit_quiz'),
)
