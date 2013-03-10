from django.conf.urls import patterns, url

from gpsweb import views

urlpatterns = patterns('',
    url(r'^$',views.UserLogin),
    url(r'^login$',views.UserLogin),
    url(r'^logout$',views.UserLogout),
    url(r'^register$', views.UserRegistration),
    url(r'^main_map$', views.main_map),
    url(r'^unit_route/(\d+)$', views.unit_route),
)