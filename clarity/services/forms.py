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

# could remove class below and merge
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attrs['step'] = '900'
        self.attrs['placeholder'] = 'Click to select a time.'
        self.format='%Y-%m-%dT%H:%M'

class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ('note','start','duration')
        widgets = {
            'start': DateTimeLocalInput(attrs={'class': 'flatpickr-15min'}),
            # 'start': forms.DateTimeInput(
            #     attrs={
            #         'type': 'datetime-local',
            #         'class': '',
            #     },
            #     format='%Y-%m-%dT%H:%M'
            # )
        }