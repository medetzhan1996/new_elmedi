from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from .models import Service, Form, ICD, Insurance, Hospital
from .forms import ServiceForm, FormForm, ICDForm
from customer.models import Customer
from customer.forms import CustomerForm


class ServiceJsonView(View):

    def get(self, request, *args, **kwargs):
        parent_id = request.GET.get('parent', None)
        parent = None if parent_id == '#' else parent_id
        services = Service.objects.filter(parent=parent).all()
        data = []
        for service in services:
            parent = service.parent.id if service.parent else '#'
            title = service.code + ' - ' + service.title
            item = {
                'id': service.id,
                'text': title,
                'parent': parent
            }
            if not service.is_leaf_node():
                item["children"] = True
            data.append(item)
        return JsonResponse(data, safe=False)


# Mixin программы
class ServiceMixin(LoginRequiredMixin):
    model = Service

    def get_success_url(self):
        parent = self.kwargs.get('parent', None)
        if parent:
            return reverse_lazy( 'directory:service_list',
                kwargs = {'parent': parent})
        return reverse_lazy('directory:service_list')


class ServiceEditMixin(ServiceMixin):
    form_class = ServiceForm


# Список услуг
class ServiceListView(ServiceMixin, ListView):
    template_name = 'directory/service/list.html'
    context_object_name = 'services'
    paginate_by = 100

    def get_queryset(self):
        parent = self.kwargs.get('parent', None)
        qs = super().get_queryset().order_by('id')
        return qs.filter(parent=parent)

    def get_context_data(self, *args, **kwargs):
        service_ancestors = []
        context = super().get_context_data(*args, **kwargs)
        parent = self.kwargs.get('parent', None)
        if parent:
            service_ancestors = get_object_or_404(Service, pk=parent).get_ancestors(include_self=True)
        context['service_ancestors'] = service_ancestors
        return context


# Добавить услугу
class ServiceCreateView(ServiceEditMixin, CreateView):
    template_name = 'directory/service/create.html'


# Обновить услугу
class ServiceUpdateView(ServiceEditMixin, UpdateView):
    template_name = 'directory/service/update.html'


# Удалить услугу
class ServiceDeleteView(ServiceMixin, DeleteView):
    template_name = 'directory/service/delete.html'



# Mixin программы
class FormMixin(LoginRequiredMixin):
    model = Form

    def get_success_url(self):
        parent = self.kwargs.get('parent', None)
        if parent:
            return reverse_lazy( 'directory:form_list',
                kwargs = {'parent': parent})
        return reverse_lazy('directory:form_list')


class FormEditMixin(FormMixin):
    form_class = FormForm


# Список услуг
class FormListView(FormEditMixin, ListView):
    template_name = 'directory/form/list.html'
    context_object_name = 'forms'
    paginate_by = 100

    def get_queryset(self):
        parent = self.kwargs.get('parent', None)
        qs = super().get_queryset().order_by('code')
        return qs.filter(parent=parent)

    def get_context_data(self, *args, **kwargs):
        form_ancestors = []
        context = super().get_context_data(*args, **kwargs)
        parent = self.kwargs.get('parent', None)
        if parent:
            form_ancestors = get_object_or_404(Form, pk=parent).get_ancestors(include_self=True).order_by('code')
        context['form_ancestors'] = form_ancestors
        return context


# Добавить услугу
class FormCreateView(FormEditMixin, CreateView):
    template_name = 'directory/form/create.html'


# Обновить услугу
class FormUpdateView(FormEditMixin, UpdateView):
    template_name = 'directory/form/update.html'


# Удалить услугу
class FormDeleteView(FormMixin, DeleteView):
    template_name = 'directory/form/delete.html'


# Mixin программы
class ICDMixin(LoginRequiredMixin):
    model = ICD

    def get_success_url(self):
        parent = self.kwargs.get('parent', None)
        if parent:
            return reverse_lazy( 'directory:icd_list',
                kwargs = {'parent': parent})
        return reverse_lazy('directory:icd_list')


class ICDEditMixin(ServiceMixin):
    form_class = ICDForm


# Список услуг
class ICDListView(ICDMixin, ListView):
    template_name = 'directory/icd/list.html'
    context_object_name = 'icds'
    paginate_by = 100

    def get_queryset(self):
        parent = self.kwargs.get('parent', None)
        qs = super().get_queryset().order_by('id')
        return qs.filter(parent=parent)

    def get_context_data(self, *args, **kwargs):
        icd_ancestors = []
        context = super().get_context_data(*args, **kwargs)
        parent = self.kwargs.get('parent', None)
        if parent:
            icd_ancestors = get_object_or_404(ICD, pk=parent).get_ancestors(include_self=True)
        context['icd_ancestors'] = icd_ancestors
        return context


# Добавить услугу
class ICDCreateView(ICDEditMixin, CreateView):
    template_name = 'directory/icd/create.html'


# Обновить услугу
class ICDUpdateView(ICDEditMixin, UpdateView):
    template_name = 'directory/icd/update.html'


# Удалить услугу
class ICDDeleteView(ICDMixin, DeleteView):
    template_name = 'directory/icd/delete.html'


# Mixin программы
class InsuranceMixin(LoginRequiredMixin):
    model = Insurance


# Список услуг
class InsuranceListView(InsuranceMixin, ListView):
    template_name = 'directory/insurance/list.html'
    context_object_name = 'insurances'
    paginate_by = 100


# Mixin программы
class HospitalMixin(LoginRequiredMixin):
    model = Hospital


# Список услуг
class HospitalListView(HospitalMixin, ListView):
    template_name = 'directory/hospital/list.html'
    context_object_name = 'hospitals'
    paginate_by = 100


# Mixin программы
class CustomerMixin(LoginRequiredMixin):
    model = Customer

    def get_success_url(self):
        return reverse_lazy('directory:customer_list')


class CustomerEditMixin(CustomerMixin):
    form_class = CustomerForm
    template_name = 'directory/customer/form.html'


# Список услуг
class CustomerListView(CustomerMixin, ListView):
    template_name = 'directory/customer/list.html'
    context_object_name = 'customers'
    paginate_by = 100


# Добавить услугу
class CustomerCreateView(CustomerEditMixin, CreateView):
    pass


# Обновить услугу
class CustomerUpdateView(CustomerEditMixin, UpdateView):
    pass


# Удалить услугу
class CustomerDeleteView(CustomerMixin, DeleteView):
    template_name = 'directory/customer/delete.html'


class AdminInsurancePageView(TemplateView):
    template_name = 'directory/admin_insurance/list.html'


class AdminHospitalPageView(TemplateView):
    template_name = 'directory/admin_hospital/list.html'


class AdminProMedicinePageView(TemplateResponseMixin, View):
    template_name = 'directory/admin_pro_medicine/list.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

class AdminProMedicineHospitalPageView(TemplateView):
    template_name = 'directory/admin_pro_medicine_hospital/list.html'
