from django.urls import path
from . import views

app_name = 'promedecine'

urlpatterns = [
    path('professional/examination/<int:iin>', views.ProfessionalExaminationApiView.as_view(),
         name='professional_examination_api'),
    path('examination/appointments/<int:customer_iin>', views.ExaminationAppointmentApiView.as_view(),
         name='examination_appointments_api'),
    path('examination/result/create', views.ExaminationResultCreateView.as_view(),
         name='examination_result_create'),
    path('examination/result/<int:customer_iin>', views.ExaminationResultApiView.as_view(),
         name='examination_result_api'),
    path('package/list/<int:customer_iin>', views.PackageListApiView.as_view(),
         name='package_list_api'),


]
