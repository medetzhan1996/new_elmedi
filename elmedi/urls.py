from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken import views

urlpatterns = i18n_patterns(
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', include('account.urls', namespace='account')),
    path('program_management/', include('program_management.urls', namespace='program_management')),
    path('package_service_management/',
         include('package_service_management.urls', namespace='package_service_management')),
    path('package_icd_management/',
         include('package_icd_management.urls', namespace='package_icd_management')),
    path('contract_management/',
         include('contract_management.urls', namespace='contract_management')),
    path('hospital_service_management/',
         include('hospital_service_management.urls', namespace='hospital_service_management')),
    path('hospital_icd_management/',
         include('hospital_icd_management.urls', namespace='hospital_icd_management')),
    path('directory/', include('directory.urls', namespace='directory')),
    path('report_management/', include('report_management.urls', namespace='report_management')),
    path('import_data/', include('import_data.urls', namespace='import_data')),
    path('promedicine/', include('promedicine.urls', namespace='promedicine')),
)

urlpatterns += [
    path('admin/', admin.site.urls),    
    path('api/customer/', include('customer.api.urls', namespace='customer_api')),
    path('api/contract_management/', include('contract_management.api.urls', namespace='contract_management_api')),
    path('api/promedicine/', include('promedicine.api.urls', namespace='promedicine_api')),
    path('api/referral_management/', include('referral_management.api.urls', namespace='referral_management_api')),
    path('api/invoice_management/', include('invoice_management.api.urls', namespace='invoice_management_api')),
    path('api/document_management/', include('document_management.api.urls', namespace='document_management_api')),
    path('api-token-auth/', views.obtain_auth_token),
    path('rosetta/', include('rosetta.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
