from django.urls import path
from . import views

app_name = 'referral_api'

urlpatterns = [
    path('list/customer/<str:search>/template', views.ReferralListByCustomerTemplate.as_view(),
         name='referral_list_by_customer'),
    path('create/customer/<str:iin>/template', views.ReferralCreateByCustomerTemplate.as_view(),
         name='referral_create_by_customer'),
    path('perform/<int:pk>/template', views.ReferralPerformTemplate.as_view(),
         name='referral_perform'),
    path('<int:pk>', views.ReferralDetail.as_view(),
         name='referral-detail'),
    path('hospital/services', views.HospitalServicesList.as_view(),
         name='hospital-services'),
    path('test/api', views.TestList.as_view(),
         name='test_api'),
]
