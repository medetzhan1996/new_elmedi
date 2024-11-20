from django import forms
from .models import Package, PackageService


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['title', 'description']


class ProMedPackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProMedPackageForm, self).__init__(*args, **kwargs)
        self.fields['insurer'].required = True

    class Meta:
        model = Package
        fields = ['title', 'description', 'insurer']


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