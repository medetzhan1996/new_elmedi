from django import forms
from .models import AttachedDocument


# Форма расписании
class AttachedDocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['screen'].widget = forms.HiddenInput()

    class Meta:
        model = AttachedDocument
        fields = ['title', 'file', 'screen', 'invoice']
