from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from directory.models import Service
from directory.models import Insurer
from .models import Package, PackageService
from .forms import PackageServiceForm, PackageForm, PackageServiceSettingForm, ProMedPackageForm


class ProMedBaseMixin:

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если в параметрах запроса есть insurer, фильтруем queryset по этому insurer
        insurer_id = self.request.GET.get('insurer')
        if insurer_id:
            queryset = queryset.filter(insurer_id=insurer_id)
        return queryset

    def get_context_data(self, **kwargs):
        # Первоначально получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем в контекст список всех страховщиков
        context['insurers'] = Insurer.objects.all()
        context['selected_insurer'] = self.request.GET.get('insurer', '')
        return context


# Mixin программы
class PackageMixin(LoginRequiredMixin):
    context_object_name = 'packages'
    paginate_by = 100
    success_url = reverse_lazy('package_service_management:package_list')

    def get_queryset(self):
        return Package.objects.filter(insurer__isnull=True)


# Mixin программы
class PackageEditMixin:
    form_class = PackageForm


class PackageListView(PackageMixin, ListView):
    template_name = 'package_service_management/package/list.html'


class PackageCreateView(PackageMixin, PackageEditMixin, CreateView):
    template_name = 'package_service_management/package/create.html'


class PackageUpdateView(PackageMixin, PackageEditMixin, UpdateView):
    template_name = 'package_service_management/package/update.html'


# Удалить
class PackageDeleteView(PackageMixin, DeleteView):
    template_name = 'package_service_management/package/delete.html'


class ProMedPackageMixin(PackageMixin, ProMedBaseMixin):
    success_url = reverse_lazy('package_service_management:pro_med_package_list')

    def get_queryset(self):
        return Package.objects.filter(insurer__isnull=False)


# ProMed Mixin программы
class ProMedPackageEditMixin:
    form_class = ProMedPackageForm


class ProMedPackageListView(ProMedPackageMixin, ListView):
    template_name = 'package_service_management/pro_med_package/list.html'


class ProMedPackageCreateView(ProMedPackageMixin, ProMedPackageEditMixin, CreateView):
    template_name = 'package_service_management/pro_med_package/create.html'


class ProMedPackageUpdateView(ProMedPackageMixin, ProMedPackageEditMixin, UpdateView):
    template_name = 'package_service_management/pro_med_package/update.html'


# Удалить
class ProMedPackageDeleteView(ProMedPackageMixin, DeleteView):
    template_name = 'package_service_management/pro_med_package/delete.html'


class PackageEvaluationListView(PackageMixin, ListView):
    template_name = 'package_service_management/package_evaluation/list.html'

class ProMedPackageEvaluationListView(ProMedPackageMixin, ListView):
    template_name = 'package_service_management/pro_med_package_evaluation/list.html'

# Mixin услуг пакета
class PackageServiceMixin(LoginRequiredMixin):
    model = Service
    context_object_name = 'services'
    package = None

    def dispatch(self, *args, **kwargs):
        self.package = get_object_or_404(Package, pk=self.kwargs.get('package'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        package_services = PackageService.objects.filter(
            package=self.package).values_list('service')
        return qs.filter(id__in=package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = self.package
        return context


# Услуги пакета
class PackageServiceListView(PackageServiceMixin, ListView):
    template_name = 'package_service_management/package_service/list.html'


# Услуги пакета
class ProMedPackageServiceListView(PackageServiceMixin, ListView):
    template_name = 'package_service_management/pro_med_package_service/list.html'


# Услуги пакета
class PackageServiceFormView(View):

    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        package_service, created = PackageService.objects.get_or_create(
            package=package, service=service
        )
        form = PackageServiceForm(request.POST, instance=package_service)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


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
class PackageServiceEvaluationListView(PackageServiceMixin, ListView):
    template_name = 'package_service_management/package_service_evaluation/list.html'

# Услуги пакета промед
class ProMedPackageServiceEvaluationListView(PackageServiceMixin, ListView):
    template_name = 'package_service_management/pro_med_package_service_evaluation/list.html'

class ServiceSettingMixin(LoginRequiredMixin):
    context_object_name = 'services'
    paginate_by = 100
    base_service = None
    model = Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = []
        base_services = Service.objects.filter(parent=None).all()
        self.base_service = self.request.GET.get('base_service', None)
        if self.base_service:
            services = Service.objects.get(pk=self.base_service).get_descendants(include_self=True)
        context['base_services'] = base_services
        context['base_service'] = self.base_service
        context['services'] = services
        return context


class PackageServiceSettingMixin(ServiceSettingMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = get_object_or_404(Package, pk=self.kwargs.get('package'))
        return context


# Услуги пакета
class PackageServiceSettingView(PackageServiceSettingMixin, ListView):
    template_name = 'package_service_management/package_service/setting.html'


class ProMedPackageServiceSettingView(PackageServiceSettingMixin, ListView):
    template_name = 'package_service_management/pro_med_package_service/setting.html'


# Услуги пакета
class ServiceSettingView(ServiceSettingMixin, ListView):
    template_name = 'package_service_management/service/setting.html'


# Услуги пакета
class ServiceSettingFormView(View):

    def post(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        package, package_created = Package.objects.get_or_create(
            title=service.title, service=service
        )
        services_without_last_children = service.get_children()
        Package.objects.filter(
            service__in=services_without_last_children
        ).delete()
        # package_service, created = PackageService.objects.get_or_create(
        #     package=package, service=service
        # )
        # data = request.POST.copy()
        # data.update({'package': package.id})
        # form = PackageServiceSettingForm(data, instance=package_service)
        # if form.is_valid():
        #     form.save()
        #     return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class PackageServiceSettingFormView(View):

    def post(self, request, *args, **kwargs):
        is_checked = request.POST.get('is_checked')
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        if is_checked == 'true':
            
            package_service, created = PackageService.objects.get_or_create(
                package=package, service=service
            )
            form = PackageServiceSettingForm(request.POST, instance=package_service)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
        elif is_checked == 'false':
            services_without_last_children = service.get_descendants(include_self=True)
            PackageService.objects.filter(
                package=package,
                service__in=services_without_last_children
            ).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})