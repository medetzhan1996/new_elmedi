from django.urls import path
from . import views

app_name = 'referral_api'

urlpatterns = [
	path('referral/create', views.ReferralCreateView.as_view(), name='referral-create'),
    path('referral/<int:pk>', views.ReferralDetail.as_view(), name='referral-detail'),
    path('referrals/<str:iin>/by_iin', views.ReferralsByIin.as_view(), name='referrals_by_iin')
    # path('referrals/', views.ReferralList.as_view(), name='referral-list'),

]
