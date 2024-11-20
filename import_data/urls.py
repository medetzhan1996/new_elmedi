from django.urls import path
from . import views
app_name = 'import_data'
urlpatterns = [
    path('service/translate', views.TranslateServiceView.as_view(), name="service_translate"),
    path('icd/', views.ImportICDView.as_view(), name="mkb10"),
    path('service/', views.ImportServiceView.as_view(), name="service"),
    path('service/django', views.ImportServiceDjangoView.as_view(), name="service_django"),
    path('state/insurance', views.ImportStateInsuranceView.as_view(), name="state_insurance"),
    path('service_stationar/', views.ImportServiceStationarView.as_view(), name="service_stationar"),

]
