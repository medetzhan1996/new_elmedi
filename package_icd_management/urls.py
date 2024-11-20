from django.urls import path
from . import views
app_name = 'package_icd_management'

urlpatterns = [
    path('package/list/', views.PackageListView.as_view(), name='package_list'),
    path('package/create/', views.PackageCreateView.as_view(), name='package_create'),
    path('package/<int:pk>/update/', views.PackageUpdateView.as_view(), name='package_update'),
    path('package/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='package_delete'),
    path('package/evaluation/list/', views.PackageEvaluationListView.as_view(), name='package_evaluation_list'),
    path('package/<int:package>/icd/list/', views.PackageICDListView.as_view(),
         name='package_icd_list'),
    path('package/<int:package>/icd/evaluation/list/', views.PackageICDEvaluationListView.as_view(),
         name='package_icd_evaluation_list'),
    path('package<int:package>/icd/setting/', views.PackageICDSettingView.as_view(), name='package_icd_setting'),
    path('package/<int:package>/icd/form/', views.PackageICDFormView.as_view(),
         name="package_icd_form"),
    path('package/<int:package>/icd/<int:icd>/form/', views.PackageICDDeleteView.as_view(),
         name="package_icd_delete"),
    path('icd/list/', views.ICDListView.as_view(), name='icd_list'),


]
