from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = [
            'service', 'icd', 'contract_customer', 'program_package',
            'referral', 'consumption', 'performing_doctor', 'hospital',
            'doctor_signature', 'screen'
        ]
