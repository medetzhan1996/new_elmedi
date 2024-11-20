from django.urls import path,reverse_lazy

from . import views
app_name = 'promedicine'
urlpatterns = [
    path('professional_examination/list', views.ProfessionalExaminationListView.as_view(),
         name='professional_examination_list'),
    path('professional_examination/create/', views.ProfessionalExaminationCreateView.as_view(),
         name='professional_examination_create'),
    path('professional_examination/import/excel', views.ProfessionalExaminationImportExcelView.as_view(),
         name='professional_examination_import_excel'),
    path('professional_examination/import/excel/confirm', views.ConfirmImportExcelView.as_view(),
         name='professional_examination_import_excel_confirm'),
    path('professional_examination/import/excel/confirm/upload', views.ConfirmImportExcelUploadView.as_view(),
         name='professional_examination_import_excel_confirm_upload'),
    path('professional_examination/<int:pk>/delete/', views.ProfessionalExaminationDeleteView.as_view(),
         name='professional_examination_delete'),
    path('professional_examination/<int:pk>/update/', views.ProfessionalExaminationUpdateView.as_view(),
         name='professional_examination_update'),
    path('api/examination/appointment/list', views.ExaminationAppointmentApiListView.as_view(),
         name='professional_examination_delete'),
]