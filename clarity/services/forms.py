from datetime import timedelta

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
            self.initial['subject'] = self.instance.subjects.all()

class SessionForm(forms.ModelForm):
    start = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'flatpickr-datetime',
            'step': '900',
            'placeholder': 'Select time and date.',
        })
    )

    class Meta:
        model = models.Session
        fields = ('start','duration','subject','note')

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

        if service:
            self.fields['subject'].queryset = models.SubjectService.objects.filter(service=service)
        else:
            self.fields['subject'].queryset = models.SubjectService.objects.none()            

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        duration = cleaned_data.get('duration')

        if start and duration:
            end = start + timedelta(minutes=duration)
            if models.Session.objects.filter(start__lt=end, end__gt=start).exists():
                self.add_error('start', 'This time overlaps an existing session.')

        return cleaned_data

class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['link']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ['title','file']

class ShareResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ['document', 'message']
