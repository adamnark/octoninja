from django.conf.urls import patterns, url
from wkhtmltopdf.views import PDFTemplateView
from gpsweb import views

urlpatterns = patterns('',
    url(r'^$',views.UserLogin),
    url(r'^login$',views.UserLogin),
    url(r'^logout$',views.UserLogout),
    url(r'^register$', views.UserRegistration),
    url(r'^main$', views.mainView),
#Alerts    
    url(r'^alerts$', views.alerts),
    url(r'^alerts_report_printer$', views.alertsReportPrinter),
    url(r'^alerts_report_csv$', views.alertsReportCsv),
#Car History       
    url(r'^car_history/(\d+)/$', views.carHistory),
    url(r'^car_history/(\d+)/(\d+)/(\d+)$', views.carHistory),
#Driver History    
	url(r'^driver_history/(\d+)/$', views.driverHistory),
    url(r'^driver_history/(\d+)/(\d+)/(\d+)$', views.driverHistory),
    url(r'^driver_history_report_csv/(\d+)/$', views.driverHistoryReportCsv),
    url(r'^driver_history_report_csv/(\d+)/(\d+)/(\d+)$', views.driverHistoryReportCsv),
    url(r'^driver_history_report_printer/(\d+)$', views.driverHistoryReportPrinter),
    url(r'^driver_history_report_printer/(\d+)/(\d+)/(\d+)$', views.driverHistoryReportPrinter),
#Global Reports
    url(r'^cars_route_report_csv/(\d+)/(\d+)$', views.carsRoutesCsv),
    url(r'^cars_route_report_printer/(\d+)/(\d+)$', views.carsRoutesPrinter),
#Perimeter    
    url(r'^perimeter$', views.perimeter),
    url(r'^set_new_area$', views.setNewArea),
    url(r'^set_cars_area$', views.setCarsArea),
    url(r'^update_area$', views.updateArea),
#Schedule Alert set
    url(r'^schedule$', views.schedule),    
    url(r'^set_new_schedule$', views.setNewScheduleProfile),
    url(r'^set_car_schedule$', views.setCarsSchedule),
    url(r'^update_schedule_profile$', views.updateScheduleProfile),
# Fuel Page
    url(r'^fuel$', views.fuel),
    url(r'^get_fuel_data/(\d+)/(\d+)$', views.get_fuel_data),
# Cars Form    
    url(r'^carsForm$', views.fuel),
#REST
    url(r'^carlocation/(\d{7})/$', views.carLocation),
    # url(r'^/export', admin.export_as_json),
    
)