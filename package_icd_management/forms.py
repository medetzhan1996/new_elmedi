from django import forms
from .models import Package, PackageICD


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['title', 'is_favorite']


class PackageICDForm(forms.ModelForm):

    class Meta:
        model = PackageICD
        fields = ['package', 'icd',
                  'social_at_home_performed', 'social_primary_health_care_performed',
                  'social_clinical_diagnostic_performed', 'social_hospital_performed',
                  'vhi_at_home_performed', 'vhi_primary_health_care_performed',
                  'vhi_clinical_diagnostic_performed', 'vhi_hospital_performed',
                  'pay_at_home_performed', 'pay_primary_health_care_performed',
                  'pay_clinical_diagnostic_performed', 'pay_hospital_performed',
                  'is_perfomed']

    def save(self, *args, **kwargs):
        form = super(PackageICDForm, self).save(commit=False)
        form.save()
        icd_descendants = form.icd.get_descendants()
        for icd_descendant in icd_descendants:
            package = form.package or None
            package_icd, created = PackageICD.objects.get_or_create(
                icd=icd_descendant, package=package)
            package_icd.social_at_home_performed = self.cleaned_data['social_at_home_performed']
            package_icd.social_primary_health_care_performed = self.cleaned_data['social_primary_health_care_performed']
            package_icd.social_clinical_diagnostic_performed = self.cleaned_data['social_clinical_diagnostic_performed']
            package_icd.social_hospital_performed = self.cleaned_data['social_hospital_performed']
            package_icd.vhi_at_home_performed = self.cleaned_data['vhi_at_home_performed']
            package_icd.vhi_primary_health_care_performed = self.cleaned_data['vhi_primary_health_care_performed']
            package_icd.vhi_clinical_diagnostic_performed = self.cleaned_data['vhi_clinical_diagnostic_performed']
            package_icd.vhi_hospital_performed = self.cleaned_data['vhi_hospital_performed']
            package_icd.pay_at_home_performed = self.cleaned_data['pay_at_home_performed']
            package_icd.pay_primary_health_care_performed = self.cleaned_data['pay_primary_health_care_performed']
            package_icd.pay_clinical_diagnostic_performed = self.cleaned_data['pay_clinical_diagnostic_performed']
            package_icd.pay_hospital_performed = self.cleaned_data['pay_hospital_performed']
            package_icd.is_perfomed = self.cleaned_data['is_perfomed']
            package_icd.save()
        return form