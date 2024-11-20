from django import forms
from package_service_management.models import Package as PackageBlank

from .models import Program, Package, PackageService


# Форма программы
class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ['title', 'limit_percent', 'premium_percent']

class ProMedProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProMedProgramForm, self).__init__(*args, **kwargs)
        self.fields['insurer'].required = True

        # Customize program_type choices to show only types 2 and 3
        self.fields['program_type'].choices = [
            choice for choice in self.fields['program_type'].choices if choice[0] in [2, 3]
        ]

    class Meta:
        model = Program
        fields = ['title', 'insurer', 'program_type']


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'description', 'program', 'limit', 'limit_type']
        widgets = {'program': forms.HiddenInput()}


class PackageServiceForm(forms.ModelForm):
    class Meta:
        model = PackageService
        fields = [
            'package', 'service', 'vhi_at_home_coefficient',
            'vhi_price', 'vhi_primary_health_care_coefficient',
            'vhi_clinical_diagnostic_coefficient', 'vhi_hospital_coefficient',
            'pay_base_price', 'pay_at_home_coefficient',
            'pay_primary_health_care_coefficient', 'pay_clinical_diagnostic_coefficient',
            'pay_hospital_coefficient', 'pay_base_price', 'is_checked', 'limit'
        ]


# Форма пакета
class PackageBlankForm(forms.ModelForm):
    package_blank = forms.ModelChoiceField(
        queryset=PackageBlank.objects.filter(insurer__isnull=True).all())

    def __init__(self, *args, **kwargs):
        self.program = kwargs.pop('program')
        super(PackageBlankForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Package
        fields = ['package_blank', 'limit', 'limit_type']
        exclude = ['title', 'description', 'program']

    def save(self, *args, **kwargs):
        form = super(PackageBlankForm, self).save(commit=False)
        package_blank = self.cleaned_data['package_blank']
        form.title = package_blank.title
        form.service = package_blank.service
        form.program = self.program
        form.description = package_blank.description
        form.save()
        package_services = package_blank.packageservice_set.all()
        for package_service in package_services:
            PackageService.objects.create(
                package=form,
                service=package_service.service,
                vhi_at_home_coefficient=package_service.vhi_at_home_coefficient,
                vhi_price=package_service.vhi_price,
                vhi_primary_health_care_coefficient=package_service.vhi_primary_health_care_coefficient,
                vhi_clinical_diagnostic_coefficient=package_service.vhi_clinical_diagnostic_coefficient,
                vhi_hospital_coefficient=package_service.vhi_hospital_coefficient,
                pay_base_price=package_service.pay_base_price,
                pay_at_home_coefficient=package_service.pay_at_home_coefficient,
                pay_primary_health_care_coefficient=package_service.pay_primary_health_care_coefficient,
                pay_clinical_diagnostic_coefficient=package_service.pay_clinical_diagnostic_coefficient,
                pay_hospital_coefficient=package_service.pay_hospital_coefficient,
                limit=package_service.limit

            )
        return form


class ProMedPackageBlankForm(PackageBlankForm):
    package_blank = forms.ModelChoiceField(queryset=PackageBlank.objects.none())

    def __init__(self, *args, **kwargs):
        insurer = kwargs.pop('insurer', None)
        super().__init__(*args, **kwargs)
        
        # If insurer is provided, filter the queryset
        if insurer:
            self.fields['package_blank'].queryset = PackageBlank.objects.filter(
                insurer__isnull=False, insurer=insurer)


    class Meta:
        model = Package
        fields = ['package_blank']


class PackageServiceSettingForm(forms.ModelForm):

    class Meta:
        model = PackageService
        fields = [
            'package', 'service', 'vhi_at_home_coefficient',
            'vhi_price', 'vhi_primary_health_care_coefficient',
            'vhi_clinical_diagnostic_coefficient', 'vhi_hospital_coefficient',
            'pay_base_price', 'pay_at_home_coefficient',
            'pay_primary_health_care_coefficient', 'pay_clinical_diagnostic_coefficient',
            'pay_hospital_coefficient', 'pay_base_price', 'is_checked', 'limit'
        ]

    def save(self, *args, **kwargs):
        form = super(PackageServiceSettingForm, self).save(commit=False)
        form.save()
        service_descendants = form.service.get_descendants()
        for service_descendant in service_descendants:
            package_service, created = PackageService.objects.get_or_create(
                service=service_descendant, package=form.package)
            package_service.vhi_at_home_coefficient = self.cleaned_data['vhi_at_home_coefficient']
            package_service.vhi_price = self.cleaned_data['vhi_price']
            package_service.vhi_primary_health_care_coefficient = self.cleaned_data['vhi_primary_health_care_coefficient']
            package_service.vhi_clinical_diagnostic_coefficient = self.cleaned_data['vhi_clinical_diagnostic_coefficient']
            package_service.vhi_hospital_coefficient = self.cleaned_data['vhi_hospital_coefficient']
            package_service.pay_base_price = self.cleaned_data['pay_base_price']
            package_service.pay_at_home_coefficient = self.cleaned_data['pay_at_home_coefficient']
            package_service.pay_primary_health_care_coefficient = self.cleaned_data['pay_primary_health_care_coefficient']
            package_service.pay_clinical_diagnostic_coefficient = self.cleaned_data['pay_clinical_diagnostic_coefficient']
            package_service.pay_hospital_coefficient = self.cleaned_data['pay_hospital_coefficient']
            package_service.pay_base_price = self.cleaned_data['pay_base_price']
            package_service.limit = self.cleaned_data['limit']
            package_service.is_checked = self.cleaned_data['is_checked']
            package_service.save()
        return form
