from django import forms
from customer.models import Customer
from contract_management.models import ContractCustomer
from .models import Referral


# Форма расписании
class ReferralForm(forms.ModelForm):

    class Meta:
        model = Referral
        fields = ['directed_hospital', 'service',
                  'doctor_full_name', 'icd', 'contract_customer']
        excludes = ('customer', 'sending_hospital')

    def __init__(self, iin, hospital=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iin = iin
        self.hospital = hospital
        self.fields['contract_customer'].queryset = ContractCustomer.objects.filter(
            customer__iin=iin)

    def save(self, commit=True):
        form = super(ReferralForm, self).save(commit=False)
        form.customer = self.cleaned_data['contract_customer'].customer
        form.sending_hospital = self.hospital
        form.save()

    def clean(self):
        cleaned_data = super(ReferralForm, self).clean()
        customer = cleaned_data.get('customer')
        contract_customer = cleaned_data.get('contract_customer')
        contract_program = contract_customer.contract_program
        contract = contract_program.contract
        program = contract_program.program
        service = cleaned_data.get('service')
        icd = cleaned_data.get('icd')
        directed_hospital = cleaned_data.get('directed_hospital')
        try:
            customer = Customer.objects.get(iin=self.iin)
            is_service_performed = program.is_service_performed(service)
            is__hospital_service_performed = directed_hospital.is_service_performed(service)
            if not is__hospital_service_performed:
                raise forms.ValidationError("Указанная больница не выполняет, данную услугу!")
            if not is_service_performed:
                raise forms.ValidationError("Указанная услуга не выполняется!")
        except Customer.DoesNotExist:
            raise forms.ValidationError(
                "Клиент с такой ИИН не существует!")


# Форма расписании
class ReferralPerformForm(forms.ModelForm):

    class Meta:
        model = Referral
        fields = ['performing_doctor']
        exclude = ('status', )

    def save(self, commit=True):
        form = super(ReferralPerformForm, self).save(commit=False)
        form.status = 1
        if commit:
            form.save()
        return form
