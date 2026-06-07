from django import forms
from . import models

class InviteForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        label="Invite Code"
    )

class StudentForm(forms.Form):
    year_choices = [
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11")
    ]

    year = forms.ChoiceField(
        choices=year_choices
    )

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