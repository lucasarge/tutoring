"""This is a forms file that holds forms that the user can fill."""

from datetime import timedelta
from django import forms
from . import models

# Form for inviting student to service.
class InviteForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        label="Invite Code"
    )

# Form for student survey to learn more about them.
class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ('student_note',)

# Form for caregiver survey to learn more about what is needed.
class CaregiverForm(forms.ModelForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=models.Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = models.Service
        fields = ('year', 'subject', 'caregiver_note')

    # Ticks all of the MultipleChoiceField objects that are already selected.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['subject'] = self.instance.subjects.all()

# Form for booking sessions of tutoring service. Extra information for the booking portion.
class SessionForm(forms.ModelForm):
    start = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'flatpickr-datetime',
            'placeholder': 'Select time and date.',
        })
    )
    class Meta:
        model = models.Session
        fields = ('start','duration','subject','note')

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

        # When selecting subject to be tutored in it just filters the subjects selected in settings.
        if service:
            self.fields['subject'].queryset = models.SubjectService.objects.filter(service=service)
        else:
            self.fields['subject'].queryset = models.SubjectService.objects.none()            

    # Error prevention to prevent double booking
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        duration = cleaned_data.get('duration')

        if start and duration:
            end = start + timedelta(minutes=duration)
            if models.Session.objects.filter(start__lt=end, end__gt=start, cancelled=False).exists():
                self.add_error('start', 'This time overlaps an existing session.')

        return cleaned_data

# Form used for tutors to upload the link to Google Meets for the session.
class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['link']

# Form used for uploading Resources to the Resource library as a tutor.
class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ['title','file']

# Form used for sharing Resources from the Resource library to a student.
class ShareResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ['document', 'message']
