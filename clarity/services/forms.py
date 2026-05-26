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

class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ('note','start','duration')
        widgets = {
            'start': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }