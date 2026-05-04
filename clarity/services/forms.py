from django import forms
from .models import RegisterService

class RegisterServiceForm(forms.ModelForm):
    class Meta:
        model = RegisterService
        fields = ["caregiver_note"]