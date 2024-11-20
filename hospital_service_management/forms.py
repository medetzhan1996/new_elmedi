from django import forms
from package_service_management.models import Package, PackageService
from .models import HospitalPackage, HospitalPackageService


# Форма пакета
class HospitalPackageForm(forms.ModelForm):

    class Meta:
        model = HospitalPackage
        fields = ['title', 'hospital']

    def save(self, commit=True):
        form = super(HospitalPackageForm, self).save(commit=False)
        form.save()
        return form


class HospitalPackageServiceForm(forms.ModelForm):

    class Meta:
        model = HospitalPackageService
        fields = [
            'hospital_package', 'service',
            'state_at_home', 'state_primary_health_care', 'state_clinical_diagnostic',
            'state_hospital', 'vhi_at_home_coefficient', 'vhi_price',
            'vhi_primary_health_care_coefficient',
            'vhi_clinical_diagnostic_coefficient', 'vhi_hospital_coefficient',
            'pay_base_price', 'pay_at_home_coefficient',
            'pay_primary_health_care_coefficient', 'pay_clinical_diagnostic_coefficient',
            'pay_hospital_coefficient', 'pay_base_price', 'is_checked'
        ]

    def save(self, commit=True):
        form = super(HospitalPackageServiceForm, self).save(commit=False)
        form.save()
        service_descendants = form.service.get_descendants()
        for service_descendant in service_descendants:
            package_service, created = HospitalPackageService.objects.get_or_create(
                service=service_descendant, hospital_package=form.hospital_package)
            package_service.state_at_home = self.cleaned_data['state_at_home']
            package_service.state_primary_health_care = self.cleaned_data['state_primary_health_care']
            package_service.state_clinical_diagnostic = self.cleaned_data['state_clinical_diagnostic']
            package_service.state_hospital = self.cleaned_data['state_hospital']
            package_service.vhi_at_home_coefficient = self.cleaned_data['vhi_at_home_coefficient']
            package_service.vhi_price = self.cleaned_data['vhi_price']
            package_service.vhi_primary_health_care_coefficient = self.cleaned_data[
                'vhi_primary_health_care_coefficient']
            package_service.vhi_clinical_diagnostic_coefficient = self.cleaned_data[
                'vhi_clinical_diagnostic_coefficient']
            package_service.vhi_hospital_coefficient = self.cleaned_data['vhi_hospital_coefficient']
            package_service.pay_base_price = self.cleaned_data['pay_base_price']
            package_service.pay_at_home_coefficient = self.cleaned_data['pay_at_home_coefficient']
            package_service.pay_primary_health_care_coefficient = self.cleaned_data[
                'pay_primary_health_care_coefficient']
            package_service.pay_clinical_diagnostic_coefficient = self.cleaned_data[
                'pay_clinical_diagnostic_coefficient']
            package_service.pay_hospital_coefficient = self.cleaned_data['pay_hospital_coefficient']
            package_service.pay_base_price = self.cleaned_data['pay_base_price']
            package_service.is_checked = self.cleaned_data['is_checked']
            package_service.save()
        return form
