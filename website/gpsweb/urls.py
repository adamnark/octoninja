from django.conf.urls import patterns, url

from gpsweb import views

urlpatterns = patterns('',
    url(r'^(?P<user_id>\d+)$', views.index, name='index')
)



