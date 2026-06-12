from django import forms
from . import models

class InviteForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        label="Invite Code"
    )

class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ('student_note',)

class CaregiverForm(forms.ModelForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=models.Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = models.Service
        fields = ('year', 'subject', 'caregiver_note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['subject'] = self.instance.subject.all()

class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ('note','start','duration')
        type = 'datetime-local'
        widgets = {
            'start': forms.DateTimeInput(attrs={
                'class': 'flatpickr-15min',
                'step': '900',
                'placeholder': 'Select time and date.',
                'format': '%Y-%m-%dT%H:%M'
            })
        }