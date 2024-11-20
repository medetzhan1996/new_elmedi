from django.urls import path
from . import views

app_name = 'report_management'

urlpatterns = [
    path('invoice/report/list/', views.InvoiceReportListView.as_view(),
        name='invoice_report_list'),
    path('invoice/report/<int:pk>/detail/', views.InvoiceReportDetailView.as_view(),
        name='invoice_report_detail'),
    path('invoice/report/hospital/<int:hospital>/list/', views.InvoiceReportListView.as_view(),
        name='invoice_report_hospital_list'),
    path('invoice_eps/report/<int:pk>/detail/', views.InvoiceEpsReportDetailView.as_view(),
        name='invoice_eps_report_detail'),
    path('act/report/list/', views.ActReportListView.as_view(),
        name='act_report_list'),
    
]
