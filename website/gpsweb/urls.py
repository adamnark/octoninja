from django.conf.urls import patterns, url
from wkhtmltopdf.views import PDFTemplateView


from gpsweb import views

urlpatterns = patterns('',
    url(r'^$',views.UserLogin),
    url(r'^login$',views.UserLogin),
    url(r'^logout$',views.UserLogout),
    url(r'^register$', views.UserRegistration),
    url(r'^main$', views.mainView),
    url(r'^alerts$', views.alerts),
    url(r'^car_history/(\d+)/$', views.carHistory),
    url(r'^car_history/(\d+)/(\d+)/(\d+)$', views.carHistory),
	url(r'^driver_history/(\d+)/$', views.driverHistory),
    url(r'^driver_history/(\d+)/(\d+)/(\d+)$', views.driverHistory),
    url(r'^driver_history_report_csv/(\d+)/$', views.driverHistoryReportCsv),
    url(r'^driver_history_report_csv/(\d+)/(\d+)/(\d+)$', views.driverHistoryReportCsv),
    url(r'^driver_history_report_printer/(\d+)$', views.driverHistoryReportPrinter),
    url(r'^driver_history_report_printer/(\d+)/(\d+)/(\d+)$', views.driverHistoryReportPrinter),
    
)