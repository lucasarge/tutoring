"""This is a forms file that holds forms that the user can fill."""

from django import forms
from . import models

# Form for creating Reviews.
class ReviewForm(forms.ModelForm):

    # Hiding stars input so that I can create a custom input.
    stars = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    # Defines what database model to link to and what fields to include.
    class Meta:
        model = models.Review
        fields = ['stars','message']