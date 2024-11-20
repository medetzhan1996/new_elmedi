from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Program, Package, PackageService
from .forms import ProgramForm, PackageForm, PackageBlankForm, PackageServiceSettingForm, ProMedProgramForm, ProMedPackageBlankForm
from package_service_management.models import PackageService as PackageServiceBlank
from directory.models import Service


# Mixin программы
class ProgramMixin(LoginRequiredMixin):
    success_url = reverse_lazy('program_management:program_list')

    def get_queryset(self):
        print('test........aaa')
        return Program.objects.filter(insurer__isnull=True)


class ProgramEditMixin:
    form_class = ProgramForm

# ProMed Mixin программы
class ProMedProgramMixin(LoginRequiredMixin):
    success_url = reverse_lazy('program_management:pro_med_program_list')

    def get_queryset(self):
        return Program.objects.filter(insurer__isnull=False)

class ProMedProgramEditMixin:
    form_class = ProMedProgramForm

# Список программы
class ProgramListView(ProgramMixin, ListView):
    template_name = 'program_management/program/list.html'
    context_object_name = 'programs'
    paginate_by = 100

class ProMedProgramListView(ProMedProgramMixin, ListView):
    template_name = 'program_management/pro_med_program/list.html'
    context_object_name = 'programs'
    paginate_by = 100


# Создать программу
class ProgramCreateView(ProgramMixin, ProgramEditMixin, CreateView):
    template_name = 'program_management/program/create.html'

class ProMedProgramCreateView(ProMedProgramMixin, ProMedProgramEditMixin, CreateView):
    template_name = 'program_management/pro_med_program/create.html'

# Обновить программу
class ProgramUpdateView(ProgramMixin, ProgramEditMixin, UpdateView):
    template_name = 'program_management/program/update.html'

class ProMedProgramUpdateView(ProMedProgramMixin, ProMedProgramEditMixin, UpdateView):
    template_name = 'program_management/pro_med_program/update.html'

# Удалить
class ProgramDeleteView(ProgramMixin, DeleteView):
    template_name = 'program_management/program/delete.html'

class ProMedProgramDeleteView(ProMedProgramMixin, DeleteView):
    template_name = 'program_management/pro_med_program/delete.html'


# Mixin программы
class ProgramPackageMixin(LoginRequiredMixin):
    model = Package
    context_object_name = 'packages'
    paginate_by = 100
    program = None

    def get_success_url(self):
        program = self.kwargs.get('program')
        return reverse_lazy('program_management:program_package_list',
                            kwargs={'program': program})

    def get_queryset(self):
        qs = super().get_queryset()
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return qs.filter(program=self.program)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program'] = self.program
        return context


# Mixin программы
class ProgramPackageEditMixin:
    form_class = PackageForm

# ProMed Mixin программы
class ProMedProgramPackageMixin(ProgramPackageMixin):
    def get_success_url(self):
        program = self.kwargs.get('program')
        return reverse_lazy('program_management:pro_med_program_package_list',
                            kwargs={'program': program})

class ProgramPackageListView(ProgramPackageMixin, ListView):
    template_name = 'program_management/program_package/list.html'

class ProMedProgramPackageListView(ProMedProgramPackageMixin, ListView):
    template_name = 'program_management/pro_med_program_package/list.html'



class ProgramPackageCreateView(ProgramPackageMixin, ProgramPackageEditMixin, CreateView):
    template_name = 'program_management/program_package/create.html'


class ProgramPackageUpdateView(ProgramPackageMixin, ProgramPackageEditMixin, UpdateView):
    template_name = 'program_management/program_package/update.html'

class ProMedProgramPackageUpdateView(ProMedProgramPackageMixin, ProgramPackageEditMixin, UpdateView):
    template_name = 'program_management/pro_med_program_package/update.html'


# Удалить
class ProgramPackageDeleteView(ProgramPackageMixin, DeleteView):
    template_name = 'program_management/program_package/delete.html'

class ProMedProgramPackageDeleteView(ProMedProgramPackageMixin, DeleteView):
    template_name = 'program_management/pro_med_program_package/delete.html'


class PackageBlankCreateView(LoginRequiredMixin, CreateView):
    template_name = 'program_management/package_blank/create.html'
    model = Package
    form_class = PackageBlankForm
    program = None

    def dispatch(self, *args, **kwargs):
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super(PackageBlankCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        program = self.kwargs.get('program')
        return reverse_lazy('program_management:program_package_list',
                            kwargs={'program': program})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program'] = self.program
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(PackageBlankCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["program"] = self.program
        return form_kwargs

class ProMedPackageBlankCreateView(PackageBlankCreateView):
    template_name = 'program_management/pro_med_package_blank/create.html'
    form_class = ProMedPackageBlankForm

    def get_success_url(self):
        program = self.kwargs.get('program')
        return reverse_lazy('program_management:pro_med_program_package_list',
                            kwargs={'program': program})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['insurer'] = self.request.GET.get('insurer')
        return kwargs

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
    template_name = 'program_management/program_package_service/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program'] = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return context

class ProMedPackageServiceListView(PackageServiceListView):
    template_name = 'program_management/pro_med_program_package_service/list.html'

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


class ProgramPackageServiceSettingMixin(LoginRequiredMixin):
    context_object_name = 'services'
    paginate_by = 100
    base_service = None
    model = Service
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        package = get_object_or_404(Package, pk=self.kwargs.get('package'))
        package_services = PackageServiceBlank.objects.filter(
            package__service=package.service).values_list('service__id')
        services = Service.objects.filter(id__in=package_services).all()
        context['services'] = services
        context['program'] = program
        context['package'] = package
        
        return context


# Услуги пакета
class ProgramPackageServiceSettingView(ProgramPackageServiceSettingMixin, ListView):
    template_name = 'program_management/program_package_service/setting.html'

class ProMedProgramPackageServiceSettingView(ProgramPackageServiceSettingMixin, ListView):
    template_name = 'program_management/pro_med_program_package_service/setting.html'


# Услуги пакета
class ProgramPackageServiceSettingFormView(View):

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
