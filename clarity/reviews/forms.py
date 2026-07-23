from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    stars = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    class Meta:
        model = models.Review
        fields = ['stars','message']