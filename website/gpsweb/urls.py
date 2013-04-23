from django.conf.urls import patterns, url

from gpsweb import views

urlpatterns = patterns('',
    url(r'^$',views.UserLogin),
    url(r'^login$',views.UserLogin),
    url(r'^logout$',views.UserLogout),
    url(r'^register$', views.UserRegistration),
    url(r'^main_map$', views.main_map),
    url(r'^unit_route/(\d+)/$', views.unit_route),
    url(r'^unit_route/(\d+)/(\d+)/(\d+)$', views.unit_route),
    url(r'^car_history/(\d+)/$', views.car_history),
    url(r'^car_history/(\d+)/(\d+)/(\d+)$', views.car_history),
    url(r'^driver_history/(\d+)/$', views.driver_history),
    url(r'^driver_history/(\d+)/(\d+)/(\d+)$', views.driver_history),
    url(r'^units_alerts/$', views.user_unit_alerts),
    url(r'^units_alerts/(\d+)/(\d+)$', views.user_unit_alerts),
    url(r'^alerts/$', views.car_alerts),
    url(r'^alerts/(\d+)/(\d+)$', views.car_alerts),
)