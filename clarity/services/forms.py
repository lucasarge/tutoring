from django import forms
from .models import Service, Subject

class InviteForm(forms.Form):

    code = forms.CharField(
        max_length=8,
        label="Invite Code"
    )

class StudentForm(forms.Form):
    class Meta:
        model = Service
        fields = ("year", "student_note")

class SubjectForm(forms.Form):
    class Meta:
        model = Subject
        fields = ("subject")

class CaregiverForm(forms.Form):
    class Meta:
        model = Service
        fields = ("caregiver_note")