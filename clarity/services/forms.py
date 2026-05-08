from django import forms

class InviteForm(forms.Form):

    code = forms.CharField(
        max_length=8,
        label="Invite Code"
    )