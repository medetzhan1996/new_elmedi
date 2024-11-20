from import_export import resources
from .models import HospitalPackageService

class HospitalPackageServiceResource(resources.ModelResource):
    class Meta:
        model = HospitalPackageService
        fields = ('service__translations__title', 'state_at_home', 'state_primary_health_care',
            'state_clinical_diagnostic', 'state_hospital', 'vhi_at_home_coefficient',
            'vhi_primary_health_care_coefficient', 'vhi_clinical_diagnostic_coefficient',
            'vhi_hospital_coefficient', 'vhi_price', 'pay_at_home_coefficient',
            'pay_primary_health_care_coefficient', 'pay_clinical_diagnostic_coefficient',
            'pay_hospital_coefficient', 'pay_base_price')