from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from directory.models import ICD
from .models import Package, PackageICD
from .forms import PackageICDForm, PackageForm


# Mixin программы
class PackageMixin(LoginRequiredMixin):
    model = Package
    success_url = reverse_lazy('package_icd_management:package_list')


# Mixin программы
class PackageEditMixin:
    form_class = PackageForm


class PackageListView(PackageMixin, ListView):
    template_name = 'package_icd_management/package/list.html'
    context_object_name = 'packages'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_favorite=True)


class PackageEvaluationListView(PackageMixin, ListView):
    template_name = 'package_icd_management/package_evaluation/list.html'
    context_object_name = 'packages'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_favorite=True)


class PackageCreateView(PackageMixin, PackageEditMixin, CreateView):
    template_name = 'package_icd_management/package/create.html'


class PackageUpdateView(PackageMixin, PackageEditMixin, UpdateView):
    template_name = 'package_icd_management/package/update.html'


# Удалить
class PackageDeleteView(PackageMixin, DeleteView):
    template_name = 'package_icd_management/package/delete.html'


class PackageICDMixin:
    model = PackageICD
    context_object_name = 'package_icds'

    def get_queryset(self):
        qs = super().get_queryset()
        self.package = get_object_or_404(Package, pk=self.kwargs.get('package'))
        return qs.filter(package=self.package)


# Услуги пакета
class PackageICDListView(PackageICDMixin, ListView):

    template_name = 'package_icd_management/package_icd/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        icds = ICD.objects.filter(
                packageicd__is_perfomed=True,
                packageicd__package=self.package
            ).all()
        context['package'] = self.kwargs.get('package')
        context['package_obj'] = self.package
        context['icds'] = icds
        return context


# Услуги пакета
class PackageICDEvaluationListView(PackageICDMixin, ListView):

    template_name = 'package_icd_management/package_icd_evaluation/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        icds = ICD.objects.filter(
                packageicd__is_perfomed=True, packageicd__package=self.package
            ).all()
        context['package'] = self.kwargs.get('package')
        context['package_obj'] = self.package
        context['icds'] = icds
        return context


# Услуги пакета
class PackageICDSettingView(PackageICDMixin, ListView):
    template_name = 'package_icd_management/package_icd/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_icd = self.request.GET.get('base_icd', None)
        base_icds = ICD.objects.filter(parent=None).all()
        if not base_icd:
            base_icd = base_icds[0].id
        icds = ICD.objects.get(pk=base_icd).get_descendants(include_self=False)
        context['package'] = self.kwargs.get('package')
        context['icds'] = icds
        context['base_icd'] = base_icd
        context['base_icds'] = base_icds
        context['package_obj'] = self.package
        return context


# Услуги пакета
class PackageICDFormView(View):

    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        icd = get_object_or_404(ICD, pk=request.POST.get('icd'))
        package_icd, created = PackageICD.objects.get_or_create(
            package=package, icd=icd
        )
        form = PackageICDForm(request.POST, instance=package_icd)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Удалить услуги пакета
class PackageICDDeleteView(View):

    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        icd = get_object_or_404(ICD, pk=kwargs.get('icd'))
        icd_descendants = icd.get_descendants(include_self=True)
        package_icd = PackageICD.objects.filter(
            package=package, icd__in=icd_descendants)
        if package_icd.exists():
            package_icd.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class ICDMixin:
    model = ICD
    context_object_name = 'icds'

    def get_queryset(self):
        qs = super().get_queryset()
        self.base_icds = qs.filter(parent=None).all()
        return self.base_icds


# Услуги пакета
class ICDListView(ICDMixin, ListView):
    template_name = 'package_icd_management/icd/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_icds = PackageICD.objects.values_list('icd', flat=True)
        icds = ICD.objects.filter(id__in=package_icds)
        context['icds'] = icds
        # base_icd = self.request.GET.get('base_icd', None)
        # if not base_icd:
        #     base_icd = self.base_icds[0].id
        # context['base_icd'] = base_icd
        # context['base_icds'] = self.base_icds
        return context
