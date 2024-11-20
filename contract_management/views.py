import os
import random
from datetime import datetime, time
import requests
import pandas as pd
import tempfile
from datetime import datetime
from collections import defaultdict

from django.conf import settings
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .resources import HospitalPackageServiceResource
from .models import Contract, ContractCustomer, ContractHospital, Program,\
    PackageService, Package, HospitalPackage, HospitalPackageService
from .forms import ContractForm, ContractCustomerForm, \
    ContractHospitalForm, ProgramForm, PackageForm, ProgramBlankForm, ProMedProgramBlankForm,\
    HospitalPackageForm, HospitalPackageServiceForm, ProMedContractCustomerForm,\
    ProfessionalExaminationForm, ExcelUploadForm, ProContractForm, ProMedContractHospitalForm
from referral_management.models import Referral
from invoice_management.models import Invoice
from package_icd_management.models import PackageICD
from directory.models import Service, Hospital, Insurance,Insurer
from customer.models import Customer
from promedicine.models import ProfessionalExamination, HazardReference,\
    ExaminationAppointment, SpecialityService


# Mixin программы
class ContractMixin(LoginRequiredMixin):
    success_url = reverse_lazy('contract_management:contract_list')

    def get_queryset(self):
        return Contract.objects.filter(insurance_type=Contract.VOLUNTARY_INSURANCE).all()


class ProMedContractMixin(LoginRequiredMixin):
    success_url = reverse_lazy('contract_management:contract_list')

    def get_queryset(self):
        return Contract.objects.filter(insurance_type=Contract.PROFESSIONAL_INSURANCE).all()


class ContractEditMixin(ContractMixin):
    form_class = ContractForm


class ProMedContractEditMixin(ProMedContractMixin):
    form_class = ProContractForm


class ContractListView(ContractMixin, ListView):
    template_name = 'contract_management/contract/list.html'
    context_object_name = 'contracts'
    paginate_by = 100


class ContractCreateView(ContractEditMixin, CreateView):
    template_name = 'contract_management/contract/create.html'


# Обновить программу
class ContractUpdateView(ContractEditMixin, UpdateView):
    template_name = 'contract_management/contract/update.html'


# Удалить
class ContractDeleteView(ContractMixin, DeleteView):
    template_name = 'contract_management/contract/delete.html'


class ProMedContractListView(ProMedContractMixin, ListView):
    template_name = 'contract_management/pro_med_contract/list.html'
    context_object_name = 'contracts'
    paginate_by = 100


class ProMedContractCreateView(ProMedContractEditMixin, CreateView):
    template_name = 'contract_management/pro_med_contract/create.html'
    success_url = reverse_lazy('contract_management:pro_med_contract_list')


# Обновить программу
class ProMedContractUpdateView(ProMedContractEditMixin, UpdateView):
    template_name = 'contract_management/pro_med_contract/update.html'
    success_url = reverse_lazy('contract_management:pro_med_contract_list')


# Удалить
class ProMedContractDeleteView(ProMedContractMixin, DeleteView):
    template_name = 'contract_management/pro_med_contract/delete.html'
    success_url = reverse_lazy('contract_management:pro_med_contract_list')


# Mixin пакета программы
class ContractProgramMixin(LoginRequiredMixin):

    def get_queryset(self):
        contract = self.kwargs.get('contract')
        return Program.objects.filter(contract=contract)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contract'] = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        return context

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:contract_program_list', kwargs={'contract': contract})


class ProMedProgramMixin(ContractProgramMixin):

    def get_queryset(self):
        contract = self.kwargs.get('contract')
        return Program.objects.filter(contract=contract)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:pro_med_contract_program_list', kwargs={'contract': contract})


class ContractProgramEditMixin(ContractProgramMixin):
    form_class = ProgramForm


class ProMedContractProgramEditMixin(ProMedProgramMixin):
    form_class = ProgramForm


# Список пакетов программы
class ContractProgramListView(ContractProgramMixin, ListView):
    template_name = 'contract_management/contract_program/list.html'
    context_object_name = 'contract_programs'


# Создать пакет программ
class ContractProgramCreateView(ContractProgramEditMixin, CreateView):
    template_name = 'contract_management/contract_program/create.html'


# Обновить программу
class ContractProgramUpdateView(ContractProgramEditMixin, UpdateView):
    template_name = 'contract_management/contract_program/update.html'


# Обновить программу
class ContractProgramDeleteView(ContractProgramMixin, DeleteView):
    template_name = 'contract_management/contract_program/delete.html'


class ProMedContractProgramListView(ProMedProgramMixin, ListView):
    template_name = 'contract_management/pro_med_contract_program/list.html'
    context_object_name = 'contract_programs'


# Создать пакет программ
class ProMedContractProgramCreateView(ProMedProgramMixin, CreateView):
    template_name = 'contract_management/pro_med_contract_program/create.html'


# Обновить программу
class ProMedContractProgramUpdateView(ProMedProgramMixin, UpdateView):
    template_name = 'contract_management/pro_med_contract_program/update.html'

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:pro_med_contract_program_list', kwargs={'contract': contract})


# Обновить программу
class ProMedContractProgramDeleteView(ProMedProgramMixin, DeleteView):
    template_name = 'contract_management/pro_med_contract_program/delete.html'

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:pro_med_contract_program_list', kwargs={'contract': contract})


class ContractResultView(TemplateResponseMixin, View):
    template_name = 'contract_management/contract_result/result.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        contract = Contract.objects.get(pk=pk)
        contract_exclusions = PackageICD.objects.filter(package_id=1).all()
        before_contract_exclusions = PackageICD.objects.filter(package_id=2).all()
        return self.render_to_response({
            'contract': contract,
            'contract_exclusions': contract_exclusions,
            'before_contract_exclusions': before_contract_exclusions
        })


# Mixin программы
class ContractProgramPackageMixin(LoginRequiredMixin):
    model = Package
    context_object_name = 'packages'
    contract = None
    program = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        program = self.kwargs.get('program')
        return reverse_lazy('contract_management:contract_program_package_list',
                            kwargs={'contract': contract, 'program': program})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contract'] = self.contract
        context['program'] = self.program
        return context


# Mixin программы
class ContractProgramPackageEditMixin(ContractProgramPackageMixin):
    form_class = PackageForm


class ContractProgramPackageListView(ContractProgramPackageMixin, ListView):
    template_name = 'contract_management/contract_program_package/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(program=self.program)


class ContractProgramPackageCreateView(ContractProgramPackageEditMixin, CreateView):
    template_name = 'contract_management/contract_program_package/create.html'

    def form_valid(self, form):
        form.instance.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super(ContractProgramPackageCreateView, self).form_valid(form)


class ContractProgramPackageUpdateView(ContractProgramPackageEditMixin, UpdateView):
    template_name = 'contract_management/contract_program_package/update.html'


# Удалить
class ContractProgramPackageDeleteView(ContractProgramPackageMixin, DeleteView):
    template_name = 'contract_management/contract_program_package/delete.html'


class ProMedContractProgramPackageListView(ContractProgramPackageMixin, ListView):
    template_name = 'contract_management/pro_med_contract_program_package/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(program=self.program)


class ProMedContractProgramPackageCreateView(ContractProgramPackageEditMixin, CreateView):
    template_name = 'contract_management/pro_med_contract_program_package/create.html'

    def form_valid(self, form):
        form.instance.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super(ProMedContractProgramPackageCreateView, self).form_valid(form)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        program = self.kwargs.get('program')
        return reverse_lazy('contract_management:pro_med_contract_program_package_list',
                            kwargs={'contract': contract, 'program': program})


class ProMedContractProgramPackageUpdateView(ContractProgramPackageEditMixin, UpdateView):
    template_name = 'contract_management/pro_med_contract_program_package/update.html'

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        program = self.kwargs.get('program')
        return reverse_lazy('contract_management:pro_med_contract_program_package_list',
                            kwargs={'contract': contract, 'program': program})


# Удалить
class ProMedContractProgramPackageDeleteView(ContractProgramPackageMixin, DeleteView):
    template_name = 'contract_management/pro_med_contract_program_package/delete.html'

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        program = self.kwargs.get('program')
        return reverse_lazy('contract_management:pro_med_contract_program_package_list',
                            kwargs={'contract': contract, 'program': program})
    

# Услуги пакета
class ContractProgramPackageServiceListView(LoginRequiredMixin, ListView):
    template_name = 'contract_management/contract_program_package_service/list.html'
    model = Service
    context_object_name = 'services'
    contract = None
    program = None
    package = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        self.package = get_object_or_404(Package, pk=self.kwargs.get('package'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        package_services = PackageService.objects.filter(
            package=self.package).values_list('service')
        return qs.filter(id__in=package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract'] = self.contract
        context['program'] = self.program
        context['package'] = self.package
        return context


class ProMedContractProgramPackageServiceListView(ContractProgramPackageServiceListView):
    template_name = 'contract_management/pro_med_contract_program_package_service/list.html'


class ContractProgramPackageResultListView(ContractProgramPackageServiceListView, ListView):
    template_name = 'contract_management/contract_result/list_result.html'


# Услуги пакета
class PackageServiceDeleteView(View):

    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        service = get_object_or_404(Service, pk=kwargs.get('service'))
        service_descendants = service.get_descendants(include_self=True)
        package_service = PackageService.objects.filter(package=package, service__in=service_descendants)
        if package_service.exists():
            package_service.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageStatusUpdate(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('pk'))
        hospital_package.status = request.POST.get('status')
        hospital_package.save()
        return JsonResponse({'success': True})


class ProgramBlankCreateView(LoginRequiredMixin, CreateView):
    template_name = 'contract_management/program_blank/create.html'
    model = Program
    form_class = ProgramBlankForm
    contract = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        return super(ProgramBlankCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:contract_program_list',
                            kwargs={'contract': contract})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract'] = self.contract
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProgramBlankCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["contract"] = self.contract
        return form_kwargs


class ProMedProgramBlankCreateView(ProgramBlankCreateView):
    template_name = 'contract_management/pro_med_program_blank/create.html'
    form_class = ProMedProgramBlankForm

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:pro_med_contract_program_list',
                            kwargs={'contract': contract})


# Mixin программы
class ContractCustomerMixin(LoginRequiredMixin):
    success_url = reverse_lazy('contract_management:contract_customer_list')

    def get_queryset(self):
        qs = ContractCustomer.objects.filter(contract__insurance_type=Contract.VOLUNTARY_INSURANCE)
        self.insurance = self.request.GET.get('insurance', None)
        self.insurer = self.request.GET.get('insurer', None)
        self.contract = self.request.GET.get('contract', None)
        self.program = self.request.GET.get('program', None)
        self.customer = self.request.GET.get('customer', None)
        if self.insurance:
            qs = qs.filter(contract__insurance__id=self.insurance)
        if self.insurer:
            qs = qs.filter(contract__insurer__id=self.insurer)
        if self.contract:
            qs = qs.filter(contract__id=self.contract)
        if self.program:
            qs = qs.filter(program__id=self.program)
        if self.customer:
            qs = qs.filter(customer__iin__icontains=self.customer)
        return qs


class ContractCustomerEditMixin(ContractCustomerMixin):
    form_class = ContractCustomerForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contracts'] = Contract.objects.filter(insurance_type=Contract.VOLUNTARY_INSURANCE).all()
        return context


# Список карт клиентов
class ContractCustomerListView(ContractCustomerMixin, ListView):
    template_name = 'contract_management/contract_customer/list.html'
    context_object_name = 'customer_cards'
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        insurances = Insurance.objects.all()
        insurer = Insurer.objects.all()
        contracts = Contract.objects.all()
        programs = Program.objects.filter(contract__insurance_type=Contract.VOLUNTARY_INSURANCE).all()
        if self.insurance:
            contracts = contracts.filter(insurance__id=self.insurance)
        if self.insurer:
            contracts = contracts.filter(insurer__id=self.insurer)
        if self.contract:
            programs = programs.filter(contract__id=self.contract)
        context['referrals'] = Program.objects.values('contract__id', 'contract__number').distinct()
        context['insurances'] = insurances
        context['insurer'] = insurer
        context['contracts'] = contracts
        context['programs'] = programs
        return context


class ContractCustomerCreateView(ContractCustomerEditMixin, CreateView):
    template_name = 'contract_management/contract_customer/create.html'


class ContractCustomerDetailView(ContractCustomerEditMixin, DetailView):
    template_name = 'contract_management/contract_customer/detail.html'
    context_object_name = 'contract_customer'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['referrals'] = Referral.objects.filter(contract_customer=self.object).all()
        context['invoices'] = Invoice.objects.filter(contract_customer=self.object).all()
        return context


class ContractCustomerDeleteView(ContractCustomerMixin, DeleteView):
    template_name = 'contract_management/contract_customer/delete.html'


# Mixin программы
class ProMedContractCustomerMixin(ContractCustomerMixin):
    success_url = reverse_lazy('contract_management:pro_med_contract_customer_list')

    def get_queryset(self):
        qs = ContractCustomer.objects.filter(contract__insurance_type=Contract.PROFESSIONAL_INSURANCE)
        self.insurance = self.request.GET.get('insurance', None)
        self.insurer = self.request.GET.get('insurer', None)
        self.contract = self.request.GET.get('contract', None)
        self.program = self.request.GET.get('program', None)
        self.customer = self.request.GET.get('customer', None)
        if self.insurance:
            qs = qs.filter(contract__insurance__id=self.insurance)
        if self.insurer:
            qs = qs.filter(contract__insurer__id=self.insurer)
        if self.contract:
            qs = qs.filter(contract__id=self.contract)
        if self.program:
            qs = qs.filter(program__id=self.program)
        if self.customer:
            qs = qs.filter(customer__iin__icontains=self.customer)
        return qs


class ProMedContractCustomerEditMixin(ProMedContractCustomerMixin):
    form_class = ProMedContractCustomerForm

    def get_success_url(self):
        return reverse_lazy('contract_management:pro_med_contract_customer_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contracts'] = Contract.objects.filter(insurance_type=Contract.PROFESSIONAL_INSURANCE).all()
        context['professional_examination_form'] = ProfessionalExaminationForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        professional_examination_form = context['professional_examination_form']

        # Проверяем, что обе формы валидны
        if form.is_valid() and professional_examination_form.is_valid():
            form_obj = form.save()
            professional_examination_form_obj = professional_examination_form.save(commit=False)
            professional_examination_form_obj.contract_customer = form_obj
            professional_examination_form_obj.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProMedContractCustomerListView(ProMedContractCustomerMixin, ListView):
    template_name = 'contract_management/pro_med_contract_customer/list.html'
    context_object_name = 'customer_cards'
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        insurances = Insurance.objects.all()
        insurer = Insurer.objects.all()
        contracts = Contract.objects.filter(insurance_type=Contract.PROFESSIONAL_INSURANCE).all()
        programs = Program.objects.filter(contract__insurance_type=Contract.PROFESSIONAL_INSURANCE).all()
        if self.insurance:
            contracts = contracts.filter(insurance__id=self.insurance)
        if self.insurer:
            contracts = contracts.filter(insurer__id=self.insurer)
        if self.contract:
            programs = programs.filter(contract__id=self.contract)
        context['referrals'] = Program.objects.values('contract__id', 'contract__number').distinct()
        context['insurances'] = insurances
        context['insurer'] = insurer
        context['contracts'] = contracts
        context['programs'] = programs
        return context


class ProMedContractCustomerCreateView(ProMedContractCustomerEditMixin, CreateView):
    template_name = 'contract_management/pro_med_contract_customer/create.html'


class ProMedContractCustomerDetailView(ProMedContractCustomerEditMixin, DetailView):
    template_name = 'contract_management/pro_med_contract_customer/detail.html'
    context_object_name = 'contract_customer'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['referrals'] = Referral.objects.filter(contract_customer=self.object).all()
        context['invoices'] = Invoice.objects.filter(contract_customer=self.object).all()
        return context


class ProMedContractCustomerDeleteView(ProMedContractCustomerMixin, DeleteView):
    template_name = 'contract_management/pro_med_contract_customer/delete.html'


# Mixin программы
class ContractHospitalMixin(LoginRequiredMixin):
    model = ContractHospital
    success_url = reverse_lazy('contract_management:contract_hospital_list')
    context_object_name = 'contract_hospitals'
    paginate_by = 100


class ContractHospitalEditMixin(ContractHospitalMixin):
    form_class = ContractHospitalForm


# Список карт клиентов
class ContractHospitalListView(ContractHospitalMixin, ListView):
    template_name = 'contract_management/contract_hospital/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.values('hospital', 'contract').distinct()


# Список карт клиентов
class ContractHospitalConfirmListView(ContractHospitalMixin, ListView):
    template_name = 'contract_management/contract_hospital_confirm/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        hospital = self.request.user.hospital
        return qs.filter(hospital=hospital).values('hospital', 'contract').distinct()


class ContractHospitalCreateView(ContractHospitalEditMixin, CreateView):
    template_name = 'contract_management/contract_hospital/create.html'


class ContractHospitalUpdateView(ContractHospitalEditMixin, UpdateView):
    template_name = 'contract_management/contract_hospital/update.html'


class ContractHospitalDeleteView(ContractHospitalMixin, DeleteView):
    template_name = 'contract_management/contract_hospital/delete.html'


# Mixin программы
class ProMedContractHospitalMixin(ContractHospitalMixin):
    success_url = reverse_lazy('contract_management:pro_med_contract_hospital_list')


class ProMedContractHospitalEditMixin(ProMedContractHospitalMixin):
    form_class = ProMedContractHospitalForm


# Список карт клиентов
class ProMedContractHospitalListView(ProMedContractHospitalMixin, ListView):
    template_name = 'contract_management/pro_med_contract_hospital/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.values('hospital', 'contract').distinct()


# Список карт клиентов
class ProMedContractHospitalConfirmListView(ProMedContractHospitalMixin, ListView):
    template_name = 'contract_management/pro_med_contract_hospital_confirm/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        hospital = self.request.user.hospital
        return qs.filter(hospital=hospital).values('hospital', 'contract').distinct()


class ProMedContractHospitalCreateView(ProMedContractHospitalEditMixin, CreateView):
    template_name = 'contract_management/pro_med_contract_hospital/create.html'


class ProMedContractHospitalUpdateView(ProMedContractHospitalEditMixin, UpdateView):
    template_name = 'contract_management/pro_med_contract_hospital/update.html'


class ProMedContractHospitalDeleteView(ProMedContractHospitalMixin, DeleteView):
    template_name = 'contract_management/pro_med_contract_hospital/delete.html'


# Получить список программ, при выборе контракта (ajax)
class ProgramByContractView(TemplateResponseMixin, View):
    template_name = 'contract_management/program_by_contract/list.html'

    def get(self, request, *args, **kwargs):
        contract = kwargs.get('contract')
        programs = Program.objects.filter(contract_id=contract)
        return self.render_to_response({'programs': programs})


class ContractHospitalPackageMixin(LoginRequiredMixin):
    model = HospitalPackage
    context_object_name = 'hospital_packages'

    def get_queryset(self):
        qs = super().get_queryset()
        contract_hospital = self.kwargs.get('contract_hospital')
        hospital = self.kwargs.get('hospital')
        return qs.filter(hospital=hospital, contract_hospital=contract_hospital)

    def get_success_url(self):
        contract_hospital = self.kwargs.get('contract_hospital')
        hospital = self.kwargs.get('hospital')
        return reverse_lazy('contract_management:contract_hospital_package_list',
                            kwargs={'hospital': hospital, 'contract_hospital': contract_hospital})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        context['contract_hospital'] = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return context


class HospitalPackageEditMixin:
    form_class = HospitalPackageForm


# Услуги пакета
class ContractHospitalPackageListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_package/list.html'

#pro med 
class ProMedContractHospitalPackageListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_pro_med/list.html'


# Обновить программу
class ContractHospitalPackageUpdateView(ContractHospitalPackageMixin, HospitalPackageEditMixin, UpdateView):
    template_name = 'contract_management/contract_hospital_package/update.html'


class ContractHospitalPackageDeleteView(ContractHospitalPackageMixin, DeleteView):
    template_name = 'contract_management/contract_hospital_package/delete.html'


class ContractHospitalPackageServiceMixin:
    model = Service
    context_object_name = 'services'
    hospital = None
    hospital_package = None
    contract_hospital = None

    def dispatch(self, *args, **kwargs):
        self.hospital = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        self.hospital_package = get_object_or_404(HospitalPackage, pk=self.kwargs.get('hospital_package'))
        self.contract_hospital = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        hospital_package_services = HospitalPackageService.objects.filter(
            hospital_package=self.hospital_package).values_list('service', flat=True)
        return qs.filter(id__in=hospital_package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = self.hospital
        context['hospital_package'] = self.hospital_package
        context['contract_hospital'] = self.contract_hospital
        return context


# Услуги пакета
class ContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_service/list.html'


#ProMed
class ProMedContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_service_pro_med/list.html'




class ContractHospitalServiceMixin:
    model = HospitalPackage
    context_object_name = 'hospital_packages'
    hospital = None
    hospital_packages = None
    contract_hospital = None

    def dispatch(self, *args, **kwargs):
        self.hospital = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        self.contract_hospital = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(contract_hospital=self.contract_hospital)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = self.hospital
        context['contract_hospital'] = self.contract_hospital
        return context


# Услуги пакета
class ContractHospitalServiceListView(ContractHospitalServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/list.html'

class ProMedContractHospitalServiceListView(ContractHospitalServiceMixin, ListView):
    template_name = 'contract_management/pro_med_contract_hospital_service/list.html'



# Услуги пакета
class ContractHospitalServiceExcelView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/excel.html'

# Услуги пакета договор
class ContractHospitalServiceTreatyListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/treaty_list.html'

class ProMedContractHospitalServiceTreatyListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/pro_med_contract_hospital_service/treaty_list.html'


# Услуги пакета
class HospitalPackageServiceFormView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        hospital_package_service, created = HospitalPackageService.objects.get_or_create(
            hospital_package=hospital_package, service=service
        )
        form = HospitalPackageServiceForm(request.POST, instance=hospital_package_service)
        print('test..........')
        print(form.errors)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})



# Услуги пакета
class HospitalPackageServiceExportView(View):

    def get(self, request, *args, **kwargs):
        contract_hospital = self.kwargs.get('contract_hospital')
        resource = HospitalPackageServiceResource()
        queryset = HospitalPackageService.objects.filter(
            hospital_package__contract_hospital__id=contract_hospital)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="persons.xls"'
        return response


# Услуги пакета
class ContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_service/list.html'


# Услуги пакета
class HospitalListView(ListView):
    model = Hospital
    context_object_name = 'hospitals'
    template_name = 'contract_management/hospital/list.html'


# Услуги пакета
class HospitalUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        is_checked = request.POST.get('is_checked', 'true')
        if is_checked == 'true':
            is_checked = True
        else:
            is_checked = False
        hospital = get_object_or_404(Hospital, pk=pk)
        hospital.is_checked =  is_checked
        hospital.save() 
        return JsonResponse({'success': True})


# Услуги пакета
class InsuranceListView(ListView):
    model = Insurance
    context_object_name = 'insurances'
    template_name = 'contract_management/insurance/list.html'


# Услуги пакета
class InsuranceUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        is_checked = request.POST.get('is_checked', 'true')
        if is_checked == 'true':
            is_checked = True
        else:
            is_checked = False
        insurance = get_object_or_404(Insurance, pk=pk)
        insurance.is_checked =  is_checked
        insurance.save() 
        return JsonResponse({'success': True})


# Услуги пакета
class ContractHospitalStatusUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        contract = request.POST.get('contract')
        hospital = request.POST.get('hospital')
        status = request.POST.get('status')
        contract_hospital = ContractHospital.objects.filter(
            contract__id=contract, hospital__id=hospital).update(status=status)
        return JsonResponse({'success': True})


class ContractCustomerImportExcelView(TemplateResponseMixin, View):
    template_name = 'contract_management/contract_customer/import_excel.html'

    def get(self, request, *args, **kwargs):
        form = ExcelUploadForm()
        contracts = Contract.objects.filter(insurance_type=Contract.PROFESSIONAL_INSURANCE).all()
        programs = Program.objects.all()
        context = {
            'form': form,
            'contracts': contracts,
            'programs': programs
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        contract = request.POST.get('contract')
        program = request.POST.get('program')
        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')
        uploaded_file = request.FILES['excel_file']
        # Сохраните файл во временное хранилище или в сессии
        fs = FileSystemStorage(location=tempfile.gettempdir())
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        request.session['file_path'] = file_path
        data = pd.read_excel(file_path)
        # Предполагаем, что вам нужны первые 5 строк для предпросмотра
        preview_data = data.head().values.tolist()
        context = {
            'contract': contract,
            'program': program,
            'begin_date': begin_date,
            'end_date': end_date,
            'preview_data': preview_data
        }
        return render(request, 'contract_management/contract_customer/confirm_import_excel.html', context)


class ContractCustomerConfirmImportExcelView(TemplateResponseMixin, View):
    template_name = 'contract_management/contract_customer/confirm_import_excel.html'

    def get(self, request, *args, **kwargs):
        file_path = request.session.get('file_path')
        if not file_path:
            return redirect('select_file')

        # Используйте pandas для чтения Excel-файла
        data = pd.read_excel(file_path)
        # Предполагаем, что вам нужны первые 5 строк для предпросмотра
        preview_data = data.head().values.tolist()
        context = {
            'preview_data': preview_data
        }
        return self.render_to_response(context)

class ContractCustomerConfirmImportExcelUploadView(View):
    def post(self, request, *args, **kwargs):
        contract = request.POST.get('contract')
        program = request.POST.get('program')
        begin_date_str = request.POST.get('begin_date')
        end_date_str = request.POST.get('end_date')
        file_path = request.session.get('file_path')
        if not file_path:
            return redirect('select_file')

        df = pd.read_excel(file_path)
        preview_data = df.head().values.tolist()

        rows_to_import = [int(key.split('_')[-1]) - 1 for key, value in request.POST.items() if "row_include_" in key and value == "include"]

        # Проверка дубликатов
        row_counts = defaultdict(int)
        for index in rows_to_import:
            row_data = df.iloc[index].tolist()
            row_tuple = tuple(row_data)
            row_counts[row_tuple] += 1

        duplicates = [list(row) for row, count in row_counts.items() if count > 1]

        if duplicates:
            context = {
                'contract': contract,
                'program': program,
                'begin_date': begin_date_str,
                'end_date': end_date_str,
                'preview_data': preview_data,
                'duplicates_set': {tuple(row) for row in duplicates},
            }
            return render(request, 'contract_management/contract_customer/confirm_import_excel.html', context)

        # Если нет дубликатов продолжаем импортировать

        begin_date = datetime.strptime(begin_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        contract = Contract.objects.get(id=contract)
        program = Program.objects.get(id=program)

        for index, row in df.iterrows():
            if index not in rows_to_import:
                continue

            customer_iin = row['customer']
            customer = Customer.objects.get(iin=customer_iin)

            contract_customer = ContractCustomer.objects.create(contract=contract, program=program, begin_date=begin_date, end_date=end_date, customer=customer)
            ProfessionalExamination.objects.create(contract_customer=contract_customer, plan_start_date=begin_date, plan_end_date=end_date)

        os.remove(file_path)
        return redirect('contract_management:pro_med_contract_customer_list')





# class ContractCustomerConfirmImportExcelUploadView(View):
#     def post(self, request, *args, **kwargs):
#         file_path = request.session.get('file_path')
#         if not file_path:
#             return redirect('select_file')
#
#         df = pd.read_excel(file_path)
#         preview_data = df.head().values.tolist()
#
#         rows_to_import = [int(key.split('_')[-1]) - 1 for key, value in request.POST.items() if "row_include_" in key and value == "include"]
#
#         # Проверка дубликатов
#         row_counts = defaultdict(int)
#         for index in rows_to_import:
#             row_data = df.iloc[index].tolist()
#             row_tuple = tuple(row_data)
#             row_counts[row_tuple] += 1
#
#         duplicates = [list(row) for row, count in row_counts.items() if count > 1]
#
#         # Проверка на существующие номера договоров
#         existing_numbers = ContractCustomer.objects.filter(number__in=[row['number'] for row in df.iloc[rows_to_import].to_dict('records')]).values_list('number', flat=True)
#
#         if duplicates or existing_numbers:
#             context = {
#                 'preview_data': preview_data,
#                 'duplicates_set': {tuple(row) for row in duplicates},
#                 'contract_customer_exists': list(existing_numbers),
#             }
#             return render(request, 'contract_management/contract_customer/confirm_import_excel.html', context)
#
#         # Если нет дубликатов или существующих номеров договоров, продолжаем импортировать
#         for index, row in df.iterrows():
#             if index not in rows_to_import:
#                 continue
#
#             contract_title = row['contract']
#             program_title = row['program']
#             number = row['number']
#             customer_iin = row['customer']
#
#             begin_date_str = row['begin_date']
#             begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
#
#             end_date_str = row['end_date']
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#
#             plan_start_date_str = row['plan_start_date']
#             plan_start_date = datetime.strptime(plan_start_date_str, '%Y-%m-%d').date()
#
#             plan_end_date_str = row['plan_end_date']
#             plan_end_date = datetime.strptime(plan_end_date_str, '%Y-%m-%d').date()
#
#             contract = Contract.objects.get(number__iexact=contract_title)
#             program = Program.objects.get(title__iexact=program_title)
#             customer = Customer.objects.get(iin=customer_iin)
#
#             #... [оставшаяся логика обработки и сохранения строки]
#
#             contract_customer = ContractCustomer.objects.create(contract=contract, program=program, number=number, begin_date=begin_date, end_date=end_date, customer=customer)
#             ProfessionalExamination.objects.create(contract_customer=contract_customer, plan_start_date=plan_start_date, plan_end_date=plan_end_date)
#
#         os.remove(file_path)
#         return redirect('contract_management:pro_med_contract_customer_list')




from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self, doctor_schedule: Dict[str, Dict]):
        self.doctor_schedule = doctor_schedule
        self.indexed_schedule = self.build_indexed_schedule()
        self.preferred_hospitals = defaultdict(str)

    def build_indexed_schedule(self) -> Dict:
        indexed_schedule = defaultdict(lambda: defaultdict(list))
        for speciality, details in self.doctor_schedule.items():
            for doctor, data in details.items():
                if doctor == 'duration':
                    continue
                hospital = data['hospital']
                for date, times in data.items():
                    if date != 'hospital':
                        dt_obj = date  # Здесь
                        for time in times:
                            indexed_schedule[dt_obj][speciality].append((time, doctor, hospital))
                for date in indexed_schedule:
                    indexed_schedule[date][speciality].sort()  # Sort slots for each speciality by time
        return indexed_schedule

    def find_best_time_slot(self, speciality: str, current_date: datetime,
                            preferred_hospital: Optional[str] = None,
                            last_appointment_end_time: Optional[str] = None) -> Optional[Tuple]:
        slots = self.indexed_schedule.get(current_date, {}).get(speciality, [])  # Здесь
        duration = self.doctor_schedule[speciality].get('duration', 30)

        for idx, (time, doctor, hospital) in enumerate(slots):
            if last_appointment_end_time:
                if preferred_hospital and hospital != preferred_hospital:
                    last_appointment_end_time = None
                else:
                    time_difference = datetime.strptime(time, "%H:%M") - datetime.strptime(last_appointment_end_time,
                                                                                           "%H:%M")
                    minutes_difference = time_difference.total_seconds() / 60
                    if minutes_difference < duration:
                        continue
            if not preferred_hospital or hospital == preferred_hospital:
                return (current_date, speciality, idx), (doctor, hospital, time)
        return None, None

    def assign_patients(self, patients: List[Tuple[str, List[str], datetime, datetime]]) -> Dict:
        schedule = defaultdict(list)

        for patient_name, required_specialities, start_date, end_date in patients:
            current_date = start_date
            patient_appointments = []
            slots_to_remove = []

            last_appointment_end_time = None

            while current_date <= end_date and required_specialities:
                for speciality in required_specialities.copy():
                    removal_key, slot = self.find_best_time_slot(speciality, current_date,
                                                                 self.preferred_hospitals[patient_name],
                                                                 last_appointment_end_time)
                    if not slot:
                        removal_key, slot = self.find_best_time_slot(speciality, current_date,
                                                                     last_appointment_end_time=last_appointment_end_time)
                    if slot:
                        doctor, hospital, time = slot
                        duration = self.doctor_schedule[speciality].get('duration', 30)
                        end_time = (datetime.strptime(time, "%H:%M") + timedelta(minutes=duration)).strftime('%H:%M')
                        last_appointment_end_time = end_time

                        patient_appointments.append((speciality, doctor, time, hospital, current_date.date()))
                        required_specialities.remove(speciality)
                        self.preferred_hospitals[patient_name] = hospital
                        slots_to_remove.append(removal_key)
                current_date += timedelta(days=1)

            for date, speciality, idx in slots_to_remove:
                del self.indexed_schedule[date][speciality][idx]

            if required_specialities:
                print(f"Warning: Patient {patient_name} couldn't be scheduled for: {', '.join(required_specialities)}")
            schedule[patient_name] = patient_appointments

        return schedule

    def print_schedule(self, patient_schedule: Dict[str, List[Tuple[str, str, str, str, datetime]]]):
        print(patient_schedule.items(), '-99999999')
        for patient, appointments in patient_schedule.items():
            print(f"{patient}:")
            for appointment in appointments:
                speciality, doctor, time, hospital, date = appointment
                professional_examination = ProfessionalExamination.objects.filter(
                    contract_customer__customer__iin=patient).first()
                datetime_combined = datetime.combine(date, datetime.strptime(time, "%H:%M").time())
                speciality_service = SpecialityService.objects.get(title=speciality)
                for service in speciality_service.services.all():
                    ExaminationAppointment.objects.create(service=service, doctor_code=doctor,
                                                          date_time=datetime_combined,
                                                          professional_examination=professional_examination)

                    json_data = {
                        'doctor_code': doctor,
                        'start_datetime': datetime_combined,
                        'customer_iin': patient
                    }

                    headers = {'Authorization': f'Token {settings.CUSTOMER_CABINET_TOKEN}'}
                    result = requests.post(f'{settings.CUSTOMER_CABINET_URL}/api/customer_personal_cabinet/schedule_create',
                                           data=json_data, headers=headers)

                    # Если вы хотите что-то делать с этим результатом, делайте это здесь
                    response_data = result.json()


class AggregateFreeSlotsView(View):

    def get(self, request):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_time = time(random_hour, random_minute)
        datetime_combined = datetime.combine(start_date, random_time)
        professional_examination = ProfessionalExamination.objects.first()
        
        service = Service.objects.first()
        ExaminationAppointment.objects.create(
            service=service,
            doctor_code='001',
            date_time=datetime_combined,
            professional_examination=professional_examination
        )

        return redirect('contract_management:pro_med_contract_customer_list')
        
        hospitals = request.GET.getlist('hospitals')
        params = {
            'specialization': specializations,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'hospitals': hospitals
        }
        results = []

        headers = {'Authorization': f'Token {settings.CUSTOMER_CABINET_TOKEN}'}
        response = requests.get(f"{settings.CUSTOMER_CABINET_URL}/api/customer_personal_cabinet/aggregat/free/slots", params=params, headers=headers)
        if response.status_code == 200:
            results.append(response.json())
            api_data = self.transform_api_data(response.json())
            patients = self.get_patient_data(program_id)
            scheduler = Scheduler(api_data)
            patient_schedule = scheduler.assign_patients(patients)
            scheduler.print_schedule(patient_schedule)
            return redirect('contract_management:pro_med_contract_customer_list')
        else:
            return redirect('contract_management:pro_med_contract_customer_list')

    def transform_api_data(self, api_data):
        transformed_data = {}

        for entry in api_data:
            for speciality, doctor_data in entry.items():
                if speciality not in transformed_data:
                    transformed_data[speciality] = {}
                for doctor, date_data in doctor_data.items():
                    if doctor != 'hospital':
                        if doctor not in transformed_data[speciality]:
                            transformed_data[speciality][doctor] = {}
                        for date, times in date_data.items():
                            if date != 'hospital' and date != 'duration':
                                dt_obj = datetime.strptime(date, "%Y-%m-%d")
                                transformed_data[speciality][doctor][dt_obj] = times
                        transformed_data[speciality][doctor]['hospital'] = 'Hospital'
                        transformed_data[speciality]['duration'] = 30

        return transformed_data

    def get_patient_data(self, program_id):
        patients = []
        contract_customers = ContractCustomer.objects.filter(program=program_id)

        for contract_customer in contract_customers:
            patient_name = contract_customer.customer.iin
            speciality_titles = self.get_speciality_services_for_contract_customers(contract_customer)
            start_date = datetime(contract_customer.begin_date.year, contract_customer.begin_date.month,
                                  contract_customer.begin_date.day)
            end_date = datetime(contract_customer.end_date.year, contract_customer.end_date.month,
                                contract_customer.end_date.day)

            patient_info = (patient_name, speciality_titles, start_date, end_date)
            patients.append(patient_info)

        return patients

    def get_speciality_services_for_contract_customers(self, contract_customer):
        speciality_titles = set()
        package = contract_customer.program.package_set.first()

        if package:
            service = package.packageservice_set.first().service
            speciality_services = SpecialityService.objects.filter(services=service)

            if speciality_services.exists():
                speciality_service_titles = speciality_services.values_list('title', flat=True)
                speciality_titles.update(speciality_service_titles)
                return list(speciality_titles)
            else:
                return list(speciality_titles)
        else:
            return list(speciality_titles)


    def get_speciality_services_by_program(self, program_id):
        speciality_titles = set()
        program = Program.objects.get(id=program_id)
        package = program.package_set.first()

        if package:
            service = package.packageservice_set.first().service
            speciality_services = SpecialityService.objects.filter(services=service)

            if speciality_services.exists():
                speciality_service_titles = speciality_services.values_list('title', flat=True)
                speciality_titles.update(speciality_service_titles)
                return list(speciality_titles)
            else:
                return list(speciality_titles)
        else:
            return list(speciality_titles)


class HazardReferenceListView(ListView):
    template_name = 'contract_management/pro_med_hazard_reference/list.html'
    model = HazardReference
    context_object_name = 'hazards'

class CustomerContractExaminationAppointmentsListView(ListView):
    template_name = 'contract_management/pro_med_contract_customer/customer_contract_examination_appointments.html'
    model = ExaminationAppointment
    context_object_name = 'examination_appointments'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.last()

