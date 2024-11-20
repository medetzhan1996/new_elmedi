from django.urls import path
from . import views
app_name = 'package_service_management'

urlpatterns = [
    path('package/list/', views.PackageListView.as_view(), name='package_list'),
    path('package/create/', views.PackageCreateView.as_view(), name='package_create'),
    path('package/<int:pk>/update/', views.PackageUpdateView.as_view(), name='package_update'),
    path('package/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='package_delete'),

    path('pro_med/package/list/', views.ProMedPackageListView.as_view(), name='pro_med_package_list'),
    path('pro_med/package/create/', views.ProMedPackageCreateView.as_view(), name='pro_med_package_create'),
    path('pro_med/package/<int:pk>/update/', views.ProMedPackageUpdateView.as_view(), name='pro_med_package_update'),
    path('pro_med/package/<int:pk>/delete/', views.ProMedPackageDeleteView.as_view(), name='pro_med_package_delete'),


    path('package/evaluation/list/', views.PackageEvaluationListView.as_view(), name='package_evaluation_list'),
    path('pro_med/package/evaluation/list/', views.ProMedPackageEvaluationListView.as_view(), name='pro_med_package_evaluation_list'),
    path('package/<int:package>/service/list/', views.PackageServiceListView.as_view(),
         name='package_service_list'),

    path('pro_med/package/<int:package>/service/list/', views.ProMedPackageServiceListView.as_view(),
         name='pro_med_package_service_list'),

    path('package/<int:package>/service/evaluation/list/', views.PackageServiceEvaluationListView.as_view(),
         name='package_service_evaluation_list'),
    path('pro_med/package/<int:package>/service/evaluation/list/', views.ProMedPackageServiceEvaluationListView.as_view(),
         name='pro_med_package_service_evaluation_list'),
    path('package/<int:package>/service/form', views.PackageServiceFormView.as_view(),
         name="package_service_form"),
    path('package/<int:package>/service/setting/form',
         views.PackageServiceSettingFormView.as_view(),
         name="package_service_setting_form"),
    path('service/setting',
         views.ServiceSettingView.as_view(),
         name="service_setting"),
    path('service/setting/form',
         views.ServiceSettingFormView.as_view(),
         name="service_setting_form"),

    path('package/<int:package>/service/setting/', views.PackageServiceSettingView.as_view(),
         name='package_service_setting'),

    path('pro_med/package/<int:package>/service/setting/', views.ProMedPackageServiceSettingView.as_view(),
         name='pro_med_package_service_setting'),

    path('package/<int:package>/service/<int:service>/delete', views.PackageServiceDeleteView.as_view(),
         name="package_service_delete"),
]
