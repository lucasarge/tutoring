from django import forms

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