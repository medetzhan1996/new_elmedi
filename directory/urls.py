from django.urls import path
from . import views
app_name = 'directory'
urlpatterns = [
    path('service/json', views.ServiceJsonView.as_view(), name="service_json"),
    path('service/list', views.ServiceListView.as_view(), name="service_list"),
    path('service/<int:parent>/list', views.ServiceListView.as_view(), name="service_list"),
    path('service/create', views.ServiceCreateView.as_view(), name="service_create"),
    path('<int:parent>/service/create', views.ServiceCreateView.as_view(), name="service_create"),
    path('service/<int:pk>/update', views.ServiceUpdateView.as_view(), name="service_update"),
    path('<int:parent>/service/<int:pk>/update', views.ServiceUpdateView.as_view(), name="service_update"),
    path('service/<int:pk>/delete', views.ServiceDeleteView.as_view(), name="service_delete"),
    path('<int:parent>/service/<int:pk>/delete', views.ServiceDeleteView.as_view(), name="service_delete"),

    path('form/list', views.FormListView.as_view(), name="form_list"),
    path('form/<int:parent>/list', views.FormListView.as_view(), name="form_list"),
    path('form/create', views.FormCreateView.as_view(), name="form_create"),
    path('<int:parent>/form/create', views.FormCreateView.as_view(), name="form_create"),
    path('form/<int:pk>/update', views.FormUpdateView.as_view(), name="form_update"),
    path('<int:parent>/form/<int:pk>/update', views.FormUpdateView.as_view(), name="form_update"),
    path('form/<int:pk>/delete', views.FormDeleteView.as_view(), name="form_delete"),
    path('<int:parent>/form/<int:pk>/delete', views.FormDeleteView.as_view(), name="form_delete"),

    path('icd/list', views.ICDListView.as_view(), name="icd_list"),
    path('icd/<int:parent>/list', views.ICDListView.as_view(), name="icd_list"),
    path('icd/create', views.ICDCreateView.as_view(), name="icd_create"),
    path('<int:parent>/icd/create', views.ICDCreateView.as_view(), name="icd_create"),
    path('icd/<int:pk>/update', views.ICDUpdateView.as_view(), name="icd_update"),
    path('<int:parent>/icd/<int:pk>/update', views.ICDUpdateView.as_view(), name="icd_update"),
    path('icd/<int:pk>/delete', views.ICDDeleteView.as_view(), name="icd_delete"),
    path('<int:parent>/icd/<int:pk>/delete', views.ICDDeleteView.as_view(), name="icd_delete"),

    path('admin/insurance', views.AdminInsurancePageView.as_view(), name="admin_insurance"),
    path('admin/hospital', views.AdminHospitalPageView.as_view(), name="admin_hospital"),
    path('admin/pro_medicine', views.AdminProMedicinePageView.as_view(), name="admin_pro_medicine"),
    path('admin/pro_medicine/hospital', views.AdminProMedicineHospitalPageView.as_view(), name="admin_pro_medicine_hospital"),

    path('insurance/list', views.InsuranceListView.as_view(), name="insurance_list"),

    path('hospital/list', views.HospitalListView.as_view(), name="hospital_list"),

    path('customer/list', views.CustomerListView.as_view(), name="customer_list"),
    path('customer/create', views.CustomerCreateView.as_view(), name="customer_create"),
    path('customer/<int:pk>/update', views.CustomerUpdateView.as_view(), name="customer_update"),
    path('customer/<int:pk>/delete', views.CustomerDeleteView.as_view(), name="customer_delete"),
    
    
]
