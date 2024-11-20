from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from directory.models import Hospital, ICD
from package_icd_management.models import PackageICD
from .models import HospitalPackage, HospitalPackageICD
from .forms import HospitalPackageForm, HospitalPackageICDForm


# Список пакетов программы
class HospitalListView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'hospital_icd_management/hospital/list.html'
    context_object_name = 'hospitals'
    ordering = ['id']


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

        return reverse_lazy('hospital_icd_management:hospital_package_list', kwargs={'hospital': hospital})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['hospital'] = self.kwargs.get('hospital')
        hospital_obj = Hospital.objects.get(pk=self.kwargs.get('hospital'))
        context['hospital_obj'] = hospital_obj
        return context


class HospitalPackageEditMixin:
    form_class = HospitalPackageForm


# Список пакетов программы
class HospitalPackageListView(HospitalPackageMixin, ListView):
    template_name = 'hospital_icd_management/hospital_package/list.html'


# Создать пакет программ
class HospitalPackageCreateView(HospitalPackageMixin, HospitalPackageEditMixin, CreateView):
    template_name = 'hospital_icd_management/hospital_package/create.html'


# Обновить программу
class HospitalPackageUpdateView(HospitalPackageMixin, HospitalPackageEditMixin, UpdateView):
    template_name = 'hospital_icd_management/hospital_package/update.html'


# Обновить программу
class HospitalPackageDeleteView(HospitalPackageMixin, DeleteView):
    template_name = 'hospital_icd_management/hospital_package/delete.html'


# Список пакетов программы
class HospitalPackageEvaluationListView(HospitalPackageMixin, ListView):
    template_name = 'hospital_icd_management/hospital_package_evaluation/list.html'


class HospitalPackageICDMixin:
    model = HospitalPackageICD
    context_object_name = 'hospital_package_icds'
    hospital_package = None

    def get_queryset(self):
        qs = super().get_queryset()
        self.hospital_package = get_object_or_404(
            HospitalPackage, pk=self.kwargs.get('hospital_package'))
        return qs.filter(hospital_package=self.hospital_package)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.icds = ICD.objects.filter(hospitalpackageicd__hospital_package=self.hospital_package).all()
        context['hospital'] = self.kwargs.get('hospital')
        context['hospital_package'] = self.kwargs.get('hospital_package')
        context['icds'] = self.icds
        context['hospital_obj'] = Hospital.objects.get(pk=self.kwargs.get('hospital'))
        context['hospital_package_obj'] = self.hospital_package
        return context


# Услуги пакета
class HospitalPackageICDListView(HospitalPackageICDMixin, ListView):
    template_name = 'hospital_icd_management/hospital_package_icd/list.html'


# Услуги пакета
class HospitalPackageICDFormView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        icd = get_object_or_404(ICD, pk=request.POST.get('icd'))
        hospital_package_icd, created = HospitalPackageICD.objects.get_or_create(
            hospital_package=hospital_package, icd=icd
        )
        form = HospitalPackageICDForm(request.POST, instance=hospital_package_icd)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageICDDeleteView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        icd = get_object_or_404(ICD, pk=kwargs.get('icd'))
        icd_descendants = icd.get_descendants(include_self=True)
        hospital_package_icd = HospitalPackageICD.objects.filter(
            hospital_package=hospital_package, icd__in=icd_descendants)
        if hospital_package_icd.exists():
            hospital_package_icd.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageICDSettingView(HospitalPackageICDMixin, ListView):
    template_name = 'hospital_icd_management/hospital_package_icd/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        icds = []
        base_icd = self.request.GET.get('base_icd', None)
        base_icds = ICD.objects.filter(parent=None).all()
        if base_icd:
            icds = ICD.objects.get(pk=base_icd).get_descendants(include_self=False)
        context['icds'] = icds
        context['base_icd'] = base_icd
        context['base_icds'] = base_icds
        return context


# Оценка услуг пакета
class HospitalPackageICDEvaluationListView(HospitalPackageICDMixin, ListView):
    template_name = 'hospital_icd_management/hospital_package_icd_evaluation/list.html'