from django import forms
from .models import AbsenceRequest

class AbsenceRequestForm(forms.ModelForm):
    class Meta:
        model = AbsenceRequest
        fields = ['date', 'reason']