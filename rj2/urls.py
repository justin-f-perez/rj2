from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
from rj2 import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.homepage, name="home_page"),
#    url(r'^account/profile/$', views.editaccount, name="edit_account"),

)
