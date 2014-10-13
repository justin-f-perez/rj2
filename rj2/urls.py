from django.conf.urls import patterns, include, url
from django.contrib import admin
from rj2 import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
        'login.html'}),
    url(r'^$', views.homepage),
    url(r'^accounts/profile/$', views.editaccount),
    url(r'^accounts/changepassword/$', views.changepassword),
)
