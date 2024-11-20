from django.urls import path
from . import views
app_name = 'hospital_icd_management'

urlpatterns = [

     path('hospital/list/', views.HospitalListView.as_view(), name='hospital_list'),

     path('hospital/<int:hospital>/package/list/', views.HospitalPackageListView.as_view(),
         name='hospital_package_list'),
     path('hospital/<int:hospital>/package/create/', views.HospitalPackageCreateView.as_view(),
         name='hospital_package_create'),
     path('hospital/<int:hospital>/package/<int:pk>/update/', views.HospitalPackageUpdateView.as_view(),
         name='hospital_package_update'),
     path('hospital/<int:hospital>/package/<int:pk>/delete/', views.HospitalPackageDeleteView.as_view(),
         name='hospital_package_delete'),

     path('hospital/<int:hospital>/package/evaluation/list/',
          views.HospitalPackageEvaluationListView.as_view(),
         name='hospital_package_evaluation_list'),

     path('hospital/<int:hospital>/package/<int:hospital_package>/icd/list/',
         views.HospitalPackageICDListView.as_view(), name='hospital_package_icd_list'),
     path('hospital/<int:hospital>/package/<int:hospital_package>/icd/evaluation/list/',
         views.HospitalPackageICDEvaluationListView.as_view(), name='hospital_package_icd_evaluation_list'),


     path('hospital/<int:hospital>/package/<int:hospital_package>/icd/setting/',
         views.HospitalPackageICDSettingView.as_view(), name='hospital_package_icd_setting'),
     path('hospital/<int:hospital>/package/<int:hospital_package>/icd/form',
         views.HospitalPackageICDFormView.as_view(), name="hospital_package_icd_form"),
     path('hospital/<int:hospital>/package/<int:hospital_package>/icd/<int:icd>/delete',
         views.HospitalPackageICDDeleteView.as_view(), name="hospital_package_icd_delete"),
]
