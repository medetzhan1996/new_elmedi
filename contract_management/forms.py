from django import forms

from .models import Contract, ContractCustomer, ContractHospital,\
    Program, Package, PackageService, HospitalPackage, HospitalPackageService

from hospital_service_management.models import HospitalPackage as HospitalPackageBlank,\
    HospitalPackageService as HospitalPackageServiceBlank
from program_management.models import Program as ProgramBlank
from directory.models import Hospital
from promedicine.models import ProfessionalExamination


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['number', 'start_date', 'end_date', 'insurer', 'insurance']
        exclude = ('insurance_type', )


class ProContractForm(ContractForm):

    def __init__(self, *args, **kwargs):
        super(ProContractForm, self).__init__(*args, **kwargs)
        self.instance.insurance_type = Contract.PROFESSIONAL_INSURANCE


class ContractCustomerForm(forms.ModelForm):

    class Meta:
        model = ContractCustomer
        fields = [
            'number', 'program', 'begin_date', 'end_date', 'type_holder',
            'customer', 'base_card'
        ]
        exclude = ('contract', )

    def save(self, commit=True):
        form = super(ContractCustomerForm, self).save(commit=False)
        contract = self.cleaned_data['program'].contract
        form.contract = contract
        form.save()
        return form


class ProMedContractCustomerForm(ContractCustomerForm):

    class Meta:
        model = ContractCustomer
        fields = [
            'number', 'program', 'begin_date', 'end_date', 'customer'
        ]
        exclude = ('contract',)

        def save(self, commit=True):
            form = super(ProMedContractCustomerForm, self).save(commit=False)
            contract = self.cleaned_data['program'].contract
            form.contract = contract
            form.save()
            return form


class ProfessionalExaminationForm(forms.ModelForm):

    class Meta:
        model = ProfessionalExamination
        fields = [
            'plan_start_date', 'plan_end_date'
        ]
        exclude = ('contract_customer', )


class ContractHospitalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(ContractHospitalForm, self).__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.filter(is_checked=True)
        self.fields['contract'].queryset = Contract.objects.filter(insurance_type=Contract.VOLUNTARY_INSURANCE)

    class Meta:
        model = ContractHospital
        fields = [
            'contract', 'hospital'
        ]

    def save(self, commit=True):
        contract = self.cleaned_data['contract']
        hospital = self.cleaned_data['hospital']
        programs = contract.program_set.all()
        for program in programs:
            form = ContractHospital.objects.create(
                    contract=contract, program=program,
                    hospital=hospital,
                    begin_date=contract.start_date, end_date=contract.end_date
                )
            hospital_package_blanks = HospitalPackageBlank.objects.filter(hospital=hospital).all()
            for hospital_package_blank in hospital_package_blanks:
                hospital_package = HospitalPackage.objects.create(
                    title=hospital_package_blank.title,
                    hospital=hospital,
                    contract_hospital=form
                )
                package_services = PackageService.objects.filter(
                    package__program=program).values_list('service', flat=True)
                hospital_service_package_blanks = HospitalPackageServiceBlank.objects.filter(
                    hospital_package=hospital_package_blank, service__id__in=package_services).all()
                for hospital_service_package_blank in hospital_service_package_blanks:
                    HospitalPackageService.objects.create(
                        service=hospital_service_package_blank.service,
                        is_checked=hospital_service_package_blank.is_checked,
                        hospital_package=hospital_package,
                        state_at_home=hospital_service_package_blank.state_at_home,
                        state_primary_health_care=hospital_service_package_blank.state_primary_health_care,
                        state_clinical_diagnostic=hospital_service_package_blank.state_clinical_diagnostic,
                        state_hospital=hospital_service_package_blank.state_hospital,
                        vhi_at_home_coefficient=hospital_service_package_blank.vhi_at_home_coefficient,
                        vhi_primary_health_care_coefficient=hospital_service_package_blank.vhi_primary_health_care_coefficient,
                        vhi_clinical_diagnostic_coefficient=hospital_service_package_blank.vhi_clinical_diagnostic_coefficient,
                        vhi_hospital_coefficient=hospital_service_package_blank.vhi_hospital_coefficient,
                        vhi_price=hospital_service_package_blank.vhi_price,
                        pay_at_home_coefficient=hospital_service_package_blank.pay_at_home_coefficient,
                        pay_primary_health_care_coefficient=hospital_service_package_blank.pay_primary_health_care_coefficient,
                        pay_clinical_diagnostic_coefficient=hospital_service_package_blank.pay_clinical_diagnostic_coefficient,
                        pay_hospital_coefficient=hospital_service_package_blank.pay_hospital_coefficient,
                        pay_base_price=hospital_service_package_blank.pay_base_price
                    )
        return self


class ProMedContractHospitalForm(ContractHospitalForm):

        def __init__(self, *args, **kwargs):
            super(ProMedContractHospitalForm, self).__init__(*args, **kwargs)
            self.fields['contract'].queryset = Contract.objects.filter(insurance_type=Contract.PROFESSIONAL_INSURANCE)


# Форма программы
class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ['title', 'limit_percent', 'premium_percent', 'contract']
        widgets = {'contract': forms.HiddenInput()}


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'limit', 'limit_type', 'description']
        exclude = ('program', )


# Форма программы
class ProgramBlankForm(forms.ModelForm):
    program_blank = forms.ModelChoiceField(queryset=ProgramBlank.objects.filter(insurer__isnull=True).all())

    def __init__(self, *args, **kwargs):
        self.contract = kwargs.pop('contract')
        super(ProgramBlankForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Program
        fields = ['program_blank']
        exclude = ['title', 'limit_percent', 'premium_percent', 'contract']
        widgets = {'contract': forms.HiddenInput()}

    def save(self, *args, **kwargs):
        form = super(ProgramBlankForm, self).save(commit=False)
        program_blank = self.cleaned_data['program_blank']
        form.title = program_blank.title
        form.limit_percent = program_blank.limit_percent
        form.premium_percent = program_blank.premium_percent
        form.contract = self.contract
        form.save()
        for package_blank in program_blank.package_set.all():
            package = Package.objects.create(
                title=package_blank.title,
                program=form,
                limit=package_blank.limit,
                limit_type=package_blank.limit_type
            )
            package_services = package_blank.packageservice_set.all()
            for package_service in package_services:
                PackageService.objects.create(
                    package=package,
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


class ProMedProgramBlankForm(ProgramBlankForm):
    program_blank = forms.ModelChoiceField(queryset=ProgramBlank.objects.filter(insurer__isnull=False).all())


# Форма пакета
class HospitalPackageForm(forms.ModelForm):

    class Meta:
        model = HospitalPackage
        fields = ['title', 'hospital', 'contract_hospital']
        widgets = {'contract_hospital': forms.HiddenInput()}


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
            'pay_hospital_coefficient', 'pay_base_price', 'is_checked',
            'hospital_at_home_coefficient', 'hospital_primary_health_care_coefficient',
            'hospital_clinical_diagnostic_coefficient', 'hospital_hospital_coefficient',
            'hospital_price', 'insurance_at_home_coefficient', 'insurance_primary_health_care_coefficient',
            'insurance_clinical_diagnostic_coefficient', 'insurance_hospital_coefficient',
            'insurance_base_price'
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
            package_service.hospital_at_home_coefficient = self.cleaned_data['hospital_at_home_coefficient']
            package_service.hospital_primary_health_care_coefficient = self.cleaned_data['hospital_primary_health_care_coefficient']
            package_service.hospital_clinical_diagnostic_coefficient = self.cleaned_data['hospital_clinical_diagnostic_coefficient']
            package_service.hospital_hospital_coefficient = self.cleaned_data['hospital_hospital_coefficient']
            package_service.hospital_price = self.cleaned_data['hospital_price']
            package_service.insurance_at_home_coefficient = self.cleaned_data['insurance_at_home_coefficient']
            package_service.insurance_primary_health_care_coefficient = self.cleaned_data['insurance_primary_health_care_coefficient']
            package_service.insurance_clinical_diagnostic_coefficient = self.cleaned_data['insurance_clinical_diagnostic_coefficient']
            package_service.insurance_hospital_coefficient = self.cleaned_data['insurance_hospital_coefficient']
            package_service.insurance_base_price = self.cleaned_data['insurance_base_price']
            package_service.save()
        return form


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()