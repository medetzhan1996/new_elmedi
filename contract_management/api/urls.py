from django.urls import path
from . import views

app_name = 'contract_management'

urlpatterns = [
    path('performed/services', views.PerformedServicesView.as_view(),
         name='performed_services'),
    path('<str:card_number>/available/hospitals', views.AvailableHospitalsView.as_view(),
         name='available_hospitals'),
    path('contract/customer/create', views.ContractCustomerCreateView.as_view(),
         name='contract_customer_create'),
    path('contract_customer/<str:number>/detail', views.ContractCustomerDetailView.as_view(),
         name='contract_customer_detail'),
    path('customer/<str:search>/contract/list', views.CustomerContractListView.as_view(),
         name='customer_contract_list'),
    path('program/list', views.ProgramListView.as_view(),
         name='program_list'),
    


]
