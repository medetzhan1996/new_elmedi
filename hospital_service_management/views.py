from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from directory.models import Hospital, Service
from .models import HospitalPackage, HospitalPackageService
from .forms import HospitalPackageForm, HospitalPackageServiceForm
from directory.forms import HospitalForm


class HospitalMixin(LoginRequiredMixin):
    model = Hospital
    context_object_name = 'hospitals'

    def get_success_url(self):
        return reverse_lazy('hospital_service_management:hospital_list')


class HospitalEditMixin:
    form_class = HospitalForm


# Список пакетов программы
class HospitalListView(HospitalMixin, ListView):
    template_name = 'hospital_service_management/hospital/list.html'
    ordering = ['id']


# Список пакетов программы
class HospitalCreateView(HospitalMixin, HospitalEditMixin, CreateView):
    template_name = 'hospital_service_management/hospital/create.html'


# Список пакетов программы
class HospitalUpdateView(HospitalMixin, HospitalEditMixin, UpdateView):
    template_name = 'hospital_service_management/hospital/update.html'


# Обновить программу
class HospitalDeleteView(HospitalMixin, DeleteView):
    template_name = 'hospital_service_management/hospital/delete.html'


# Mixin пакета программы
class HospitalPackageMixin(LoginRequiredMixin):
    model = HospitalPackage
    context_object_name = 'hospital_packages'

    def get_queryset(self):
        qs = super().get_queryset()
        hospital = self.kwargs.get('hospital')
        return qs.filter(hospital=hospital)

    def get_success_url(self):
        hospital = self.kwargs.get('hospital')

        return reverse_lazy('hospital_service_management:hospital_package_list', kwargs={'hospital': hospital})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        return context


class HospitalPackageEditMixin:
    form_class = HospitalPackageForm


# Список пакетов программы
class HospitalPackageListView(HospitalPackageMixin, ListView):
    template_name = 'hospital_service_management/hospital_package/list.html'


# Создать пакет программ
class HospitalPackageCreateView(HospitalPackageMixin, HospitalPackageEditMixin, CreateView):
    template_name = 'hospital_service_management/hospital_package/create.html'


# Обновить программу
class HospitalPackageUpdateView(HospitalPackageMixin, HospitalPackageEditMixin, UpdateView):
    template_name = 'hospital_service_management/hospital_package/update.html'


# Обновить программу
class HospitalPackageDeleteView(HospitalPackageMixin, DeleteView):
    template_name = 'hospital_service_management/hospital_package/delete.html'

#Pro med
class HospitalProMedPackageMixin(HospitalPackageMixin):
     def get_success_url(self):
        hospital = self.kwargs.get('hospital')

        return reverse_lazy('hospital_service_management:hospital_pro_med_package_list', kwargs={'hospital': hospital})

class HospitalPackageProMedListView(HospitalProMedPackageMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_pro_med/list.html'

class HospitalPackageProMedCreateView(HospitalProMedPackageMixin, HospitalPackageEditMixin, CreateView):
    template_name = 'hospital_service_management/hospital_package_pro_med/create.html'

class HospitalPackageProMedUpdateView(HospitalProMedPackageMixin, HospitalPackageEditMixin, UpdateView):
    template_name = 'hospital_service_management/hospital_package_pro_med/update.html'

class HospitalPackageProMedDeleteView(HospitalProMedPackageMixin, DeleteView):
    template_name = 'hospital_service_management/hospital_package_pro_med/delete.html'

class HospitalPackageProMedEvaluationListView(HospitalPackageMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_evaluation_pro_med/list.html'


# Список пакетов программы
class HospitalPackageEvaluationListView(HospitalPackageMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_evaluation/list.html'


class HospitalPackageServiceMixin:
    model = Service
    context_object_name = 'services'
    hospital = None
    hospital_package = None

    def dispatch(self, *args, **kwargs):
        self.hospital = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        self.hospital_package = get_object_or_404(HospitalPackage, pk=self.kwargs.get('hospital_package'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        hospital_package_services = HospitalPackageService.objects.filter(
            hospital_package=self.hospital_package).values_list('service')
        return qs.filter(id__in=hospital_package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = self.hospital
        context['hospital_package'] = self.hospital_package
        return context


# Услуги пакета
class HospitalPackageServiceListView(HospitalPackageServiceMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_service/list.html'
#Pro med

class HospitalPackageProMedServiceListView(HospitalPackageServiceMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_service_pro_med/list.html'
# Услуги пакета
class HospitalPackageServiceFormView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        hospital_package_service, created = HospitalPackageService.objects.get_or_create(
            hospital_package=hospital_package, service=service
        )
        form = HospitalPackageServiceForm(request.POST, instance=hospital_package_service)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageServiceDeleteView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        service = get_object_or_404(Service, pk=kwargs.get('service'))
        service_descendants = service.get_descendants(include_self=True)
        hospital_package_service = HospitalPackageService.objects.filter(
            hospital_package=hospital_package, service__in=service_descendants)
        if hospital_package_service.exists():
            hospital_package_service.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageServiceSettingView(LoginRequiredMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_service/setting.html'
    context_object_name = 'services'

    def get_queryset(self):
        services = []
        base_service = self.request.GET.get('base_service', None)
        if base_service:
            services = Service.objects.get(pk=base_service).get_descendants(include_self=True)
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_services = Service.objects.filter(parent=None).all()
        context['base_service'] = self.request.GET.get('base_service', None)
        context['base_services'] = base_services
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        context['hospital_package'] = get_object_or_404(HospitalPackage, pk=self.kwargs.get('hospital_package'))
        return context

#ProMed
class HospitalPackageProMedServiceSettingView(HospitalPackageServiceSettingView):
    template_name = 'hospital_service_management/hospital_package_service_pro_med/setting.html'

# Оценка услуг пакета
class HospitalPackageServiceEvaluationListView(HospitalPackageServiceMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_service_evaluation/list.html'

#ProMed
class HospitalPackageProMedServiceEvaluationListView(HospitalPackageServiceMixin, ListView):
    template_name = 'hospital_service_management/hospital_package_service_evaluation_pro_med/list.html'
#
#
# class ContractHospitalPackageMixin(LoginRequiredMixin):
#     model = HospitalPackage
#     context_object_name = 'hospital_packages'
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         contract_hospital = self.kwargs.get('contract_hospital')
#         hospital = self.kwargs.get('hospital')
#         return qs.filter(hospital=hospital, contract_hospital=contract_hospital)
#
#     def get_success_url(self):
#         contract_hospital = self.kwargs.get('contract_hospital')
#         hospital = self.kwargs.get('hospital')
#         return reverse_lazy('hospital_service_management:contract_hospital_package_list',
#                             kwargs={'hospital': hospital, 'contract_hospital': contract_hospital})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['hospital'] = get_object_or_404(Hospital, self.kwargs.get('hospital'))
#         context['contract_hospital'] = self.kwargs.get('contract_hospital')
#         return context
#
#
# # Услуги пакета
# class ContractHospitalPackageListView(ContractHospitalPackageMixin, ListView):
#     template_name = 'hospital_service_management/contract_hospital_package/list.html'
#
#
# # Обновить программу
# class ContractHospitalPackageUpdateView(ContractHospitalPackageMixin, HospitalPackageEditMixin, UpdateView):
#     template_name = 'hospital_service_management/contract_hospital_package/update.html'
#
#
# class ContractHospitalPackageServiceMixin(HospitalPackageServiceMixin):
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['contract_hospital'] = self.kwargs.get('contract_hospital')
#         return context
#
#
# # Обновить программу
# class ContractHospitalPackageDeleteView(ContractHospitalPackageMixin, DeleteView):
#     template_name = 'hospital_service_management/contract_hospital_package/delete.html'
#
#
# # Услуги пакета
# class ContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
#     template_name = 'hospital_service_management/contract_hospital_package_service/list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         contract_hospital = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
#         # contract = Contract.objects.get(pk=1)
#         # TYPE_APPEAL_CHOICES = (
#         #     ('social', 'ОМС'),
#         #     ('vhi', 'ДМС'),
#         #     ('pay', 'Платно'),
#         # )
#         # type_appeal = ''
#         # icd_code = ''
#         # place = ''
#         # package_icd = PackageICD.objects.filter(icd__code=icd_code).first()
#         # if package_icd:
#         #     if not package_icd.social_at_home_performed:
#         # contract = Contract.objects.get(pk=1)
#         # services = get_performed_services(contract)
#         # print(services)
#
#         program = contract_hospital.contract_program.program
#         package_services = list(PackageService.objects.filter(
#             package__programpackage__program=program).values_list('service__id', flat=True))
#
#         services = self.services.filter(id__in=package_services)
#         context['services'] = services
#         context['program'] = program
#         return context
