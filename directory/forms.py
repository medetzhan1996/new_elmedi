from django import forms
from parler.forms import TranslatableModelForm
from .models import Service, Form, Hospital, ICD


class ServiceForm(TranslatableModelForm):

    class Meta:
        model = Service
        fields = ['title', 'code', 'parent']


class ICDForm(TranslatableModelForm):

    class Meta:
        model = ICD
        fields = ['title', 'code', 'parent']


class FormForm(TranslatableModelForm):

    class Meta:
        model = Form
        fields = ['title', 'code', 'file', 'parent']


class HospitalForm(forms.ModelForm):

    class Meta:
        model = Hospital
        fields = ['title', 'logo']