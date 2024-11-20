from django import forms
from .models import ProfessionalExamination


class ProfessionalExaminationForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExamination
        fields = ['contract_customer', 'plan_start_date', 'status']


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
