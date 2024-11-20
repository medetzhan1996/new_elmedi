from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .filters import InvoiceFilter
from invoice_management.models import Invoice, InvoiceEPSDMS


# Mixin программы
class InvoiceReportMixin(LoginRequiredMixin):
    model = Invoice


class InvoiceReportListView(InvoiceReportMixin, ListView):
    template_name = 'report_management/invoice/list.html'
    context_object_name = 'invoices'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        hospital = self.kwargs.get('hospital', None)
        if hospital:
            return qs.filter(hospital__id=hospital)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        invoices = Invoice.objects.all()
        context['filter'] = InvoiceFilter(self.request.GET, queryset=invoices)
        context['invoice_eps_dms'] = InvoiceEPSDMS.objects.all()
        return context


class InvoiceReportDetailView(InvoiceReportMixin, DetailView):
    template_name = 'report_management/invoice/detail.html'
    context_object_name = 'invoice'



class InvoiceEpsReportDetailView(DetailView):
    model = InvoiceEPSDMS
    template_name = 'report_management/invoice/detail_eps.html'
    context_object_name = 'invoice'


class ActReportListView(InvoiceReportMixin,ListView):
    template_name = 'report_management/act/list.html'
    context_object_name = 'invoices'
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        invoices = Invoice.objects.all()
        context['filter'] = InvoiceFilter(self.request.GET, queryset=invoices)
        context['invoice_eps_dms'] = InvoiceEPSDMS.objects.all()
        return context
