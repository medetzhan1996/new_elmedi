from django.urls import path
from . import views

app_name = 'invoice_api'

urlpatterns = [
    path('invoice/create', views.InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoice_eps_dms/create', views.InvoiceEPSDMSCreateView.as_view(), name='invoice-eps_dms-create'),
]
